using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using System.Drawing;
using System.Drawing.Imaging;


namespace Classes
{
    public interface IOSDisplay
    {
        void Init(int height, int width);
        void RawCopy(byte[] videoRam, int videoRamSize);
    }

    public enum TextRegion
    {
        NormalBottom,
        Normal2,
        CombatSummary,
    }

    public class Display
    {
        static byte[,] OrigEgaColors = { { 0, 0, 0 }, { 0, 0, 173 }, { 0, 173, 0 }, { 0, 173, 173 }, { 173, 0, 0 }, { 173, 0, 173 }, { 173, 82, 0 }, { 173, 173, 173 }, { 82, 82, 82 }, { 82, 82, 255 }, { 82, 255, 82 }, { 82, 255, 255 }, { 255, 82, 82 }, { 255, 82, 255 }, { 255, 255, 82 }, { 255, 255, 255 } };
        static byte[,] egaColors = { { 0, 0, 0 }, { 0, 0, 173 }, { 0, 173, 0 }, { 0, 173, 173 }, { 173, 0, 0 }, { 173, 0, 173 }, { 173, 82, 0 }, { 173, 173, 173 }, { 82, 82, 82 }, { 82, 82, 255 }, { 82, 255, 82 }, { 82, 255, 255 }, { 255, 82, 82 }, { 255, 82, 255 }, { 255, 255, 82 }, { 255, 255, 255 } };
        static int[,] ram;
        static byte[] videoRam;
        static byte[] videoRamBkUp;
        static int videoRamSize;
        static int scanLineWidth;
        static int outputWidth;
        static int outputHeight;
        
        static public Bitmap bm;
        public sealed class ExternalImageLayer
        {
            public string Key;
            public string Path;
            public Bitmap Image;
            public Rectangle LogicalRect;
            public int Order;
        }

        const string DefaultExternalImageKey = "default";
        static public Bitmap ExternalImage;
        static public Rectangle ExternalImageLogicalRect;
        public static readonly object ExternalImageLock = new object();
        static readonly Dictionary<string, ExternalImageLayer> externalImages =
            new Dictionary<string, ExternalImageLayer>();
        static Rectangle rect = new Rectangle(0, 0, 320, 200);

        public struct HighResGlyph
        {
            public int GlyphIndex;
            public int ForegroundColor;
        }

        static readonly object highResFontLock = new object();
        static readonly Dictionary<int, HighResGlyph> highResGlyphs = new Dictionary<int, HighResGlyph>();
        static Bitmap highResFontAtlas;

        public delegate void VoidDeledate();

        static VoidDeledate updateCallback;

        static public VoidDeledate UpdateCallback
        {
            set
            {
                updateCallback = value;
            }
        }

        static Display()
        {
            outputHeight = 200;
            outputWidth = 320;

            ram = new int[outputHeight, outputWidth];
            scanLineWidth = outputWidth * 3;
            videoRamSize = scanLineWidth * outputHeight;
            videoRam = new byte[videoRamSize];

            bm = new Bitmap(outputWidth, outputHeight, PixelFormat.Format24bppRgb);
        }

        static int[] MonoBitMask = { 0x80, 0x40, 0x20, 0x10, 0x08, 0x04, 0x02, 0x01 };

        public static void DisplayMono8x8(int xCol, int yCol, byte[] monoData8x8, int bgColor, int fgColor)
        {
            int pX = xCol * 8;
            bool highResFont = HighResFontAvailable;

            for (int yStep = 0; yStep < 8; yStep++)
            {
                int pY = (yCol * 8) + yStep;
                int value = gbl.monoCharData[yStep];

                for (int i = 0; i < 8; i++)
                {
                    // The HD glyph is drawn as a presentation layer. Suppress
                    // its low-resolution foreground pixels in the framebuffer
                    // so rounding at non-integer display scales cannot expose a
                    // second pixel font underneath it.
                    ram[pY, pX + i] = (value & MonoBitMask[i]) != 0 && highResFont
                        ? bgColor
                        : ((value & MonoBitMask[i]) != 0 ? fgColor : bgColor);
                    SetVidPixel(pX + i, pY, ram[pY, pX + i]);
                }
            }
        }

        public static bool HighResFontAvailable
        {
            get
            {
                lock (highResFontLock)
                {
                    if (highResFontAtlas == null)
                    {
                        string root = String.IsNullOrEmpty(gbl.exe_path) ? Directory.GetCurrentDirectory() : gbl.exe_path;
                        string path = Path.Combine(root, "HDAssets", "coab-font-atlas.png");
                        if (System.IO.File.Exists(path))
                        {
                            highResFontAtlas = new Bitmap(path);
                        }
                    }
                    return highResFontAtlas != null;
                }
            }
        }

        public static Bitmap HighResFontAtlas
        {
            get
            {
                HighResFontAvailable.ToString();
                return highResFontAtlas;
            }
        }

        public static Dictionary<int, HighResGlyph> GetHighResGlyphSnapshot()
        {
            lock (highResFontLock)
            {
                return new Dictionary<int, HighResGlyph>(highResGlyphs);
            }
        }

        public static void QueueHighResGlyph(int glyphIndex, int xCol, int yCol, int bgColor, int fgColor)
        {
            if (!HighResFontAvailable || xCol < 0 || xCol >= 40 || yCol < 0 || yCol >= 25)
            {
                return;
            }
            lock (highResFontLock)
            {
                highResGlyphs[yCol * 40 + xCol] = new HighResGlyph
                {
                    GlyphIndex = glyphIndex,
                    ForegroundColor = fgColor
                };
            }
        }

        public static void ClearHighResText(int yStart, int yEnd, int xStart, int xEnd)
        {
            lock (highResFontLock)
            {
                for (int y = Math.Max(0, yStart); y <= Math.Min(24, yEnd); y++)
                {
                    for (int x = Math.Max(0, xStart); x <= Math.Min(39, xEnd); x++)
                    {
                        highResGlyphs.Remove(y * 40 + x);
                    }
                }
            }
        }

        static void InvalidateHighResText(Rectangle logicalRect)
        {
            if (logicalRect.Width <= 0 || logicalRect.Height <= 0)
            {
                lock (highResFontLock)
                {
                    highResGlyphs.Clear();
                }
                return;
            }

            ClearHighResText(
                logicalRect.Top / 8,
                (logicalRect.Bottom - 1) / 8,
                logicalRect.Left / 8,
                (logicalRect.Right - 1) / 8);
        }

        public static Color GetEgaColor(int index)
        {
            index = Math.Max(0, Math.Min(15, index));
            return Color.FromArgb(egaColors[index, 0], egaColors[index, 1], egaColors[index, 2]);
        }

        public static void SetEgaPalette(int index, int colour)
        {
            egaColors[index, 0] = OrigEgaColors[colour, 0];
            egaColors[index, 1] = OrigEgaColors[colour, 1];
            egaColors[index, 2] = OrigEgaColors[colour, 2];

            for (int y = 0; y < outputHeight; y++)
            {
                int vy = y * scanLineWidth;
                for (int x = 0; x < outputWidth; x++)
                {
                    int vx = x * 3;
                    int egaColor = ram[y, x];

                    videoRam[vy + vx + 0] = egaColors[egaColor, 2];
                    videoRam[vy + vx + 1] = egaColors[egaColor, 1];
                    videoRam[vy + vx + 2] = egaColors[egaColor, 0];
                }
            }

            Display.Update();
        }

        static void SetVidPixel(int x, int y, int egaColor)
        {
            videoRam[(y * scanLineWidth) + (x * 3) + 0] = egaColors[egaColor, 2];
            videoRam[(y * scanLineWidth) + (x * 3) + 1] = egaColors[egaColor, 1];
            videoRam[(y * scanLineWidth) + (x * 3) + 2] = egaColors[egaColor, 0];
        }

        static int noUpdateCount;

        public static void UpdateStop()
        {
            noUpdateCount++;
        }

        public static void UpdateStart()
        {
            noUpdateCount--;
            Update();
        }

        static public void Update()
        {
            if (noUpdateCount == 0)
            {
                RawCopy(videoRam, videoRamSize);

                if (updateCallback != null)
                {
                    updateCallback.Invoke();
                }
            }
        }

        static public void ForceUpdate()
        {
            RawCopy(videoRam, videoRamSize);

            if (updateCallback != null)
            {
                updateCallback.Invoke();
            }
        }

        public static void SetExternalImage(string path)
        {
            SetExternalImage(path, Rectangle.Empty, true);
        }

        public static void SetExternalImage(string path, Rectangle logicalRect)
        {
            SetExternalImage(path, logicalRect, true);
        }

        public static void SetExternalImage(string path, Rectangle logicalRect, bool publishImmediately)
        {
            SetExternalImage(DefaultExternalImageKey, path, logicalRect, publishImmediately);
        }

        static int ExternalImageOrder(string key)
        {
            if (key == "title-base") return 0;
            if (key == "title-overlay-3") return 1;
            if (key == "title-overlay-4") return 2;
            if (key == "bigpic") return 10;
            if (key == "game-picture") return 20;
            if (key == "portrait-head") return 30;
            if (key == "portrait-body") return 31;
            return 100;
        }

        public static void SetExternalImage(string key, string path, Rectangle logicalRect, bool publishImmediately)
        {
            if (String.IsNullOrEmpty(key))
            {
                key = DefaultExternalImageKey;
            }

            lock (ExternalImageLock)
            {
                ExternalImageLayer current;
                if (externalImages.TryGetValue(key, out current) &&
                    String.Equals(current.Path, path, StringComparison.OrdinalIgnoreCase) &&
                    current.LogicalRect == logicalRect)
                {
                    return;
                }
            }

            Bitmap replacement = new Bitmap(path);
            ExternalImageLayer previous = null;
            lock (ExternalImageLock)
            {
                externalImages.TryGetValue(key, out previous);
                externalImages[key] = new ExternalImageLayer
                {
                    Key = key,
                    Path = path,
                    Image = replacement,
                    LogicalRect = logicalRect,
                    Order = ExternalImageOrder(key)
                };

                if (key == DefaultExternalImageKey)
                {
                    ExternalImage = replacement;
                    ExternalImageLogicalRect = logicalRect;
                }
            }

            // Each retained layer replaces only its own logical rectangle.
            // Preserve unrelated HD text, including the party Name/AC/HP box.
            InvalidateHighResText(logicalRect);

            if (previous != null && previous.Image != null)
            {
                previous.Image.Dispose();
            }

            if (publishImmediately && updateCallback != null)
            {
                updateCallback.Invoke();
            }
        }

        public static void ClearExternalImage()
        {
            ClearExternalImage(true);
        }

        public static void ClearExternalImage(bool publishImmediately)
        {
            ClearAllExternalImages(publishImmediately);
        }

        public static void ClearExternalImage(string key, bool publishImmediately)
        {
            ExternalImageLayer previous = null;
            lock (ExternalImageLock)
            {
                if (externalImages.TryGetValue(key, out previous))
                {
                    externalImages.Remove(key);
                }

                if (key == DefaultExternalImageKey)
                {
                    ExternalImage = null;
                    ExternalImageLogicalRect = Rectangle.Empty;
                }
            }

            if (previous != null && previous.Image != null)
            {
                InvalidateHighResText(previous.LogicalRect);
                previous.Image.Dispose();
            }

            if (publishImmediately && previous != null)
            {
                ForceUpdate();
            }
        }

        public static void ClearAllExternalImages(bool publishImmediately)
        {
            List<ExternalImageLayer> previous;
            lock (ExternalImageLock)
            {
                previous = new List<ExternalImageLayer>(externalImages.Values);
                externalImages.Clear();
                ExternalImage = null;
                ExternalImageLogicalRect = Rectangle.Empty;
            }

            foreach (ExternalImageLayer layer in previous)
            {
                InvalidateHighResText(layer.LogicalRect);
                if (layer.Image != null)
                {
                    layer.Image.Dispose();
                }
            }

            if (publishImmediately && previous.Count > 0)
            {
                ForceUpdate();
            }
        }

        public static List<ExternalImageLayer> GetExternalImageSnapshot()
        {
            lock (ExternalImageLock)
            {
                List<ExternalImageLayer> snapshot = new List<ExternalImageLayer>(externalImages.Values);
                snapshot.Sort(delegate(ExternalImageLayer left, ExternalImageLayer right)
                {
                    return left.Order.CompareTo(right.Order);
                });
                return snapshot;
            }
        }

        public static void SaveVidRam()
        {
            videoRamBkUp = (byte[])videoRam.Clone();
        }

        public static void RestoreVidRam()
        {
            videoRam = videoRamBkUp;
        }

        public static byte GetPixel(int x, int y)
        {
            return (byte)ram[y, x];
        }

        public static void SetPixel3(int x, int y, int value)
        {
            if (value < 16)
            {
                // Opaque picture/symbol pixels replace whatever occupied this
                // logical cell in the original framebuffer. Retire any cached
                // HD glyph for that cell at the same replacement boundary.
                lock (highResFontLock)
                {
                    highResGlyphs.Remove((y / 8) * 40 + (x / 8));
                }

                ram[y, x] = value;

                SetVidPixel(x, y, ram[y, x]);
            }
            if (value > 16)
            {
            }
        }


      
        public static void RawCopy(byte[] videoRam, int videoRamSize)
        {
            System.Drawing.Imaging.BitmapData bmpData =
                bm.LockBits(rect, System.Drawing.Imaging.ImageLockMode.WriteOnly,
                System.Drawing.Imaging.PixelFormat.Format24bppRgb);

            IntPtr ptr = bmpData.Scan0;

            System.Runtime.InteropServices.Marshal.Copy(videoRam, 0, ptr, videoRamSize);

            bm.UnlockBits(bmpData);
        }
    }
}
