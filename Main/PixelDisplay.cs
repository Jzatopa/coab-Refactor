using System;
using System.Drawing;
using System.Drawing.Drawing2D;
using System.Drawing.Imaging;
using System.Windows.Forms;

namespace Main
{
    // Presents the original 320x200 framebuffer at a modern display size
    // without changing the game's coordinate system or artwork.
    public class PixelDisplay : PictureBox
    {
        public PixelDisplay()
        {
            BackColor = Color.Black;
            SizeMode = PictureBoxSizeMode.Normal;
            SetStyle(ControlStyles.UserPaint |
                     ControlStyles.AllPaintingInWmPaint |
                     ControlStyles.OptimizedDoubleBuffer, true);
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

            if (Classes.Display.ExternalImage != null)
            {
                Rectangle logicalRect = Classes.Display.ExternalImageLogicalRect;
                e.Graphics.CompositingMode = CompositingMode.SourceOver;

                if (logicalRect.IsEmpty)
                {
                    e.Graphics.DrawImage(
                        Classes.Display.ExternalImage,
                        new Rectangle(left, top, width, height),
                        0,
                        0,
                        Classes.Display.ExternalImage.Width,
                        Classes.Display.ExternalImage.Height,
                        GraphicsUnit.Pixel);
                }
                else
                {
                    Rectangle destination = new Rectangle(
                        left + (int)System.Math.Round(logicalRect.X * scale),
                        top + (int)System.Math.Round(logicalRect.Y * scale),
                        (int)System.Math.Round(logicalRect.Width * scale),
                        (int)System.Math.Round(logicalRect.Height * scale));

                    e.Graphics.DrawImage(
                        Classes.Display.ExternalImage,
                        destination,
                        0,
                        0,
                        Classes.Display.ExternalImage.Width,
                        Classes.Display.ExternalImage.Height,
                        GraphicsUnit.Pixel);
                }
            }

            DrawHighResolutionText(e.Graphics, left, top, scale);
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
            graphics.InterpolationMode = InterpolationMode.HighQualityBicubic;
            graphics.PixelOffsetMode = PixelOffsetMode.HighQuality;

            foreach (var entry in glyphs)
            {
                int yCol = entry.Key / 40;
                int xCol = entry.Key % 40;
                int glyphIndex = entry.Value.GlyphIndex;
                if (glyphIndex < 0 || glyphIndex >= 64)
                {
                    continue;
                }

                Color color = Classes.Display.GetEgaColor(entry.Value.ForegroundColor);
                using (ImageAttributes attributes = new ImageAttributes())
                {
                    ColorMatrix tint = new ColorMatrix(new float[][]
                    {
                        new float[] { 0, 0, 0, 0, color.R / 255f },
                        new float[] { 0, 0, 0, 0, color.G / 255f },
                        new float[] { 0, 0, 0, 0, color.B / 255f },
                        new float[] { 0, 0, 0, 1, 0 },
                        new float[] { 0, 0, 0, 0, 1 }
                    });
                    attributes.SetColorMatrix(tint, ColorMatrixFlag.Default, ColorAdjustType.Bitmap);

                    Rectangle source = new Rectangle(
                        (glyphIndex % 8) * 128,
                        (glyphIndex / 8) * 128,
                        128,
                        128);
                    Rectangle destination = new Rectangle(
                        left + (int)Math.Round(xCol * 8 * scale),
                        top + (int)Math.Round(yCol * 8 * scale),
                        (int)Math.Round(8 * scale),
                        (int)Math.Round(8 * scale));

                    graphics.DrawImage(
                        atlas,
                        destination,
                        source.X,
                        source.Y,
                        source.Width,
                        source.Height,
                        GraphicsUnit.Pixel,
                        attributes);
                }
            }
        }
    }
}
