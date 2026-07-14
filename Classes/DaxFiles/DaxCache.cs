using System;
using System.Collections.Generic;
using System.Text;

namespace Classes.DaxFiles
{
    public class DaxCache
    {
        static Dictionary<string, DaxFileCache> fileCache = new Dictionary<string, DaxFileCache>();

        public static byte[] LoadDax(string file_name, int block_id)
        {
            DaxFileCache dfc;

            string cacheKey = file_name.ToLowerInvariant();

            // The original game runs on a case-insensitive filesystem.  The
            // Linux/Mono port must still find the shipped uppercase DAX files
            // when reconstructed engine code asks for names such as 8x8d1.dax.
            if (!System.IO.File.Exists(file_name))
            {
                string directory = System.IO.Path.GetDirectoryName(file_name);
                if (String.IsNullOrEmpty(directory))
                {
                    directory = ".";
                }

                string requestedName = System.IO.Path.GetFileName(file_name);
                foreach (string candidate in System.IO.Directory.GetFiles(directory))
                {
                    if (String.Equals(System.IO.Path.GetFileName(candidate), requestedName,
                        StringComparison.OrdinalIgnoreCase))
                    {
                        file_name = candidate;
                        break;
                    }
                }
            }

            if (!fileCache.TryGetValue(cacheKey, out dfc))
            {
                dfc = new DaxFileCache(file_name);
                fileCache.Add(cacheKey, dfc);
            }

            return dfc.GetData(block_id);
        }
    }
}
