using Classes;
using System;
using System.Collections.Generic;
using System.IO;

namespace engine
{
    internal sealed class HdAssetEntry
    {
        internal string Identity;
        internal string Archive;
        internal int Block;
        internal int Frame;
        internal int Width;
        internal int Height;
        internal string Lifecycle;
        internal string Path;
    }

    internal static class HdAssetCatalog
    {
        static readonly object catalogLock = new object();
        static readonly Dictionary<string, HdAssetEntry> entries = new Dictionary<string, HdAssetEntry>();
        static string loadedRoot;

        internal static string Key(string archive, int block, int frame)
        {
            return String.Format("{0}:{1:000}:{2:000}", archive.ToUpperInvariant(), block, frame);
        }

        static void EnsureLoaded()
        {
            string root = String.IsNullOrEmpty(gbl.exe_path) ? Directory.GetCurrentDirectory() : gbl.exe_path;
            lock (catalogLock)
            {
                if (String.Equals(root, loadedRoot, StringComparison.OrdinalIgnoreCase))
                {
                    return;
                }

                entries.Clear();
                loadedRoot = root;
                string manifest = System.IO.Path.Combine(root, "HDAssets", "runtime-lookup.tsv");
                if (!System.IO.File.Exists(manifest))
                {
                    return;
                }

                string[] lines = System.IO.File.ReadAllLines(manifest);
                for (int index = 1; index < lines.Length; index++)
                {
                    string[] fields = lines[index].Split('\t');
                    if (fields.Length < 21 || fields[18] != "integrated" || String.IsNullOrEmpty(fields[19]))
                    {
                        continue;
                    }

                    int block;
                    int frame;
                    int width;
                    int height;
                    if (!Int32.TryParse(fields[3], out block) ||
                        !Int32.TryParse(fields[4], out frame) ||
                        !Int32.TryParse(fields[5], out width) ||
                        !Int32.TryParse(fields[6], out height))
                    {
                        continue;
                    }

                    string path = System.IO.Path.Combine(root, "HDAssets", fields[19].Replace('/', System.IO.Path.DirectorySeparatorChar));
                    if (!System.IO.File.Exists(path))
                    {
                        continue;
                    }

                    HdAssetEntry entry = new HdAssetEntry
                    {
                        Identity = fields[0],
                        Archive = fields[1],
                        Block = block,
                        Frame = frame,
                        Width = width,
                        Height = height,
                        Lifecycle = fields[14],
                        Path = path
                    };
                    entries[entry.Identity] = entry;
                }
            }
        }

        internal static bool TryGet(string archive, int block, int frame, out HdAssetEntry entry)
        {
            EnsureLoaded();
            lock (catalogLock)
            {
                return entries.TryGetValue(Key(archive, block, frame), out entry);
            }
        }
    }
}
