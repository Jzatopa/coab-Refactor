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
        static public Bitmap ExternalImage;
        static public Rectangle ExternalImageLogicalRect;
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
                    ram[pY, pX + i] = (value & MonoBitMask[i]) != 0 && highResFont ? bgColor :
                        ((value & MonoBitMask[i]) != 0 ? fgColor : bgColor);
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
                bool available = HighResFontAvailable;
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
            if (HighResFontAvailable == false || xCol < 0 || xCol >= 40 || yCol < 0 || yCol >= 25)
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
            SetExternalImage(path, Rectangle.Empty);
        }

        public static void SetExternalImage(string path, Rectangle logicalRect)
        {
            Bitmap replacement = new Bitmap(path);
            Bitmap previous = ExternalImage;
            ExternalImage = replacement;
            ExternalImageLogicalRect = logicalRect;

            if (previous != null)
            {
                previous.Dispose();
            }

            if (updateCallback != null)
            {
                updateCallback.Invoke();
            }
        }

        public static void ClearExternalImage()
        {
            Bitmap previous = ExternalImage;
            ExternalImage = null;
            ExternalImageLogicalRect = Rectangle.Empty;

            if (previous != null)
            {
                previous.Dispose();
            }

            ForceUpdate();
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
