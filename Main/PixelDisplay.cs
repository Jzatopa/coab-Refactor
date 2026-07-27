using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Collections.Generic;
using System.Windows.Forms;

namespace Main
{
    // Presents the original 320x200 framebuffer at a modern display size
    // without changing the game's coordinate system or artwork.
    public class PixelDisplay : PictureBox
    {
        const double HighResGlyphPresentationScale = 0.95;

        // Cache each glyph/color/output-size raster. Mono/libgdiplus applies
        // filtered alpha edges even when Graphics requests nearest-neighbor,
        // so the final-size bitmap is built with explicit integer sampling and
        // then copied unscaled.
        static readonly object rasterizedGlyphLock = new object();
        static readonly Dictionary<long, Bitmap> rasterizedGlyphs = new Dictionary<long, Bitmap>();

        public PixelDisplay()
        {
            BackColor = Color.Black;
            SizeMode = PictureBoxSizeMode.Normal;
            SetStyle(ControlStyles.UserPaint |
                     ControlStyles.AllPaintingInWmPaint |
                     ControlStyles.OptimizedDoubleBuffer, true);

        }

        static Bitmap GetRasterizedGlyph(
            Bitmap atlas, int glyphIndex, Color color, int width, int height)
        {
            ulong packedKey = ((ulong)(uint)color.ToArgb() << 26) |
                ((ulong)(uint)(glyphIndex & 0x3f) << 20) |
                ((ulong)(uint)(width & 0x3ff) << 10) |
                (uint)(height & 0x3ff);
            long key = unchecked((long)packedKey);

            lock (rasterizedGlyphLock)
            {
                Bitmap cached;
                if (rasterizedGlyphs.TryGetValue(key, out cached))
                {
                    return cached;
                }

                Bitmap rasterized = new Bitmap(width, height, PixelFormat.Format32bppArgb);
                int sourceLeft = (glyphIndex % 8) * 128;
                int sourceTop = (glyphIndex / 8) * 128;
                for (int gy = 0; gy < height; gy++)
                {
                    int sourceY = sourceTop + ((gy * 128) / height);
                    for (int gx = 0; gx < width; gx++)
                    {
                        int sourceX = sourceLeft + ((gx * 128) / width);
                        Color sourcePixel = atlas.GetPixel(sourceX, sourceY);
                        rasterized.SetPixel(
                            gx, gy,
                            Color.FromArgb(sourcePixel.A, color.R, color.G, color.B));
                    }
                }

                rasterizedGlyphs.Add(key, rasterized);
                return rasterized;
            }
        }

        static void DrawHighResolutionText(Graphics graphics, int left, int top, float scale)
        {
            Bitmap atlas = Classes.Display.HighResFontAtlas;
            if (atlas == null)
            {
                return;
            }

            var glyphs = Classes.Display.GetHighResGlyphSnapshot();
            graphics.CompositingMode = CompositingMode.SourceOver;
            // Keep the faithful bitmap atlas binary at presentation time.
            // Final-size glyphs are sampled manually and copied unscaled so
            // libgdiplus cannot add partially transparent fringe pixels. This
            // affects queued runtime text on every screen; title artwork
            // remains an independent retained-image layer.

            foreach (var entry in glyphs)
            {
                int yCol = entry.Key / 40;
                int xCol = entry.Key % 40;
                int glyphIndex = entry.Value.GlyphIndex;
                if (glyphIndex < 0 || glyphIndex >= 64) continue;

                Color color = Classes.Display.GetEgaColor(entry.Value.ForegroundColor);
                int destinationLeft = left + (int)Math.Round(xCol * 8 * scale);
                int destinationTop = top + (int)Math.Round(yCol * 8 * scale);
                int destinationRight = left + (int)Math.Round((xCol + 1) * 8 * scale);
                int destinationBottom = top + (int)Math.Round((yCol + 1) * 8 * scale);
                int destinationWidth = destinationRight - destinationLeft;
                int destinationHeight = destinationBottom - destinationTop;
                int glyphWidth = Math.Max(
                    1, (int)Math.Round(destinationWidth * HighResGlyphPresentationScale));
                int glyphHeight = Math.Max(
                    1, (int)Math.Round(destinationHeight * HighResGlyphPresentationScale));
                int glyphLeft = destinationLeft + ((destinationWidth - glyphWidth) / 2);
                int glyphTop = destinationTop + ((destinationHeight - glyphHeight) / 2);
                Bitmap rasterizedGlyph = GetRasterizedGlyph(
                    atlas, glyphIndex, color, glyphWidth, glyphHeight);
                graphics.DrawImageUnscaled(rasterizedGlyph, glyphLeft, glyphTop);
            }
        }

        protected override void OnPaint(PaintEventArgs e)
        {
            e.Graphics.Clear(Color.Black);

            if (Image == null || ClientSize.Width <= 0 || ClientSize.Height <= 0)
            {
                return;
            }

            float scale = System.Math.Min(
                ClientSize.Width / (float)Image.Width,
                ClientSize.Height / (float)Image.Height);

            int width = (int)System.Math.Round(Image.Width * scale);
            int height = (int)System.Math.Round(Image.Height * scale);
            int left = (ClientSize.Width - width) / 2;
            int top = (ClientSize.Height - height) / 2;

            e.Graphics.InterpolationMode = InterpolationMode.NearestNeighbor;
            e.Graphics.PixelOffsetMode = PixelOffsetMode.Half;
            e.Graphics.CompositingMode = CompositingMode.SourceCopy;
            e.Graphics.DrawImage(
                Image,
                new Rectangle(left, top, width, height),
                0,
                0,
                Image.Width,
                Image.Height,
                GraphicsUnit.Pixel);

            lock (Classes.Display.ExternalImageLock)
            {
                var externalImages = Classes.Display.GetExternalImageSnapshot();
                foreach (Classes.Display.ExternalImageLayer layer in externalImages)
                {
                    if (layer.Image != null)
                    {
                        Rectangle logicalRect = layer.LogicalRect;
                        e.Graphics.CompositingMode = CompositingMode.SourceOver;
                        // HD art is photographic/re-rendered artwork; keep the
                        // low-resolution game framebuffer pixel-perfect, but
                        // avoid nearest-neighbor stair-stepping on replacements.
                        e.Graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
                        e.Graphics.PixelOffsetMode = PixelOffsetMode.HighQuality;

                        if (logicalRect.IsEmpty)
                        {
                            e.Graphics.DrawImage(
                                layer.Image,
                                new Rectangle(left, top, width, height),
                                0, 0, layer.Image.Width,
                                layer.Image.Height, GraphicsUnit.Pixel);
                        }
                        else
                        {
                            Rectangle destination = new Rectangle(
                                left + (int)System.Math.Round(logicalRect.X * scale),
                                top + (int)System.Math.Round(logicalRect.Y * scale),
                                (int)System.Math.Round(logicalRect.Width * scale),
                                (int)System.Math.Round(logicalRect.Height * scale));

                            e.Graphics.DrawImage(
                                layer.Image, destination, 0, 0,
                                layer.Image.Width,
                                layer.Image.Height, GraphicsUnit.Pixel);
                        }
                    }
                }
            }
            DrawHighResolutionText(e.Graphics, left, top, scale);
        }
    }
}
