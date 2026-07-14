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
        // The same atlas glyph/color combinations are painted repeatedly.
        // Cache the tinted cells so repainting the 2K presentation does not
        // perform thousands of GetPixel/SetPixel calls every frame.
        static readonly object tintedGlyphLock = new object();
        static readonly Dictionary<long, Bitmap> tintedGlyphs = new Dictionary<long, Bitmap>();

        public PixelDisplay()
        {
            BackColor = Color.Black;
            SizeMode = PictureBoxSizeMode.Normal;
            SetStyle(ControlStyles.UserPaint |
                     ControlStyles.AllPaintingInWmPaint |
                     ControlStyles.OptimizedDoubleBuffer, true);

        }

        static Bitmap GetTintedGlyph(Bitmap atlas, int glyphIndex, Color color)
        {
            long key = ((long)glyphIndex << 32) | (uint)color.ToArgb();

            lock (tintedGlyphLock)
            {
                Bitmap cached;
                if (tintedGlyphs.TryGetValue(key, out cached))
                {
                    return cached;
                }

                Bitmap tinted = new Bitmap(128, 128, PixelFormat.Format32bppArgb);
                Rectangle source = new Rectangle((glyphIndex % 8) * 128, (glyphIndex / 8) * 128, 128, 128);
                for (int gy = 0; gy < 128; gy++)
                {
                    for (int gx = 0; gx < 128; gx++)
                    {
                        Color sourcePixel = atlas.GetPixel(source.X + gx, source.Y + gy);
                        tinted.SetPixel(gx, gy, Color.FromArgb(sourcePixel.A, color.R, color.G, color.B));
                    }
                }

                tintedGlyphs.Add(key, tinted);
                return tinted;
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
            graphics.InterpolationMode = InterpolationMode.NearestNeighbor;
            graphics.PixelOffsetMode = PixelOffsetMode.Half;

            foreach (var entry in glyphs)
            {
                int yCol = entry.Key / 40;
                int xCol = entry.Key % 40;
                int glyphIndex = entry.Value.GlyphIndex;
                if (glyphIndex < 0 || glyphIndex >= 64) continue;

                Color color = Classes.Display.GetEgaColor(entry.Value.ForegroundColor);
                Bitmap tintedGlyph = GetTintedGlyph(atlas, glyphIndex, color);
                int destinationLeft = left + (int)Math.Round(xCol * 8 * scale);
                int destinationTop = top + (int)Math.Round(yCol * 8 * scale);
                int destinationRight = left + (int)Math.Round((xCol + 1) * 8 * scale);
                int destinationBottom = top + (int)Math.Round((yCol + 1) * 8 * scale);
                Rectangle destination = new Rectangle(
                    destinationLeft, destinationTop,
                    destinationRight - destinationLeft,
                    destinationBottom - destinationTop);
                graphics.DrawImage(tintedGlyph, destination, 0, 0, tintedGlyph.Width, tintedGlyph.Height, GraphicsUnit.Pixel);
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
