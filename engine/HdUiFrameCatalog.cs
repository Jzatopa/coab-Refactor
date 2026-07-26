using Classes;
using System.Drawing;
using System.IO;

namespace engine
{
    internal static class HdUiFrameCatalog
    {
        internal static void Show(string layout)
        {
            string root = string.IsNullOrEmpty(gbl.exe_path) ? Directory.GetCurrentDirectory() : gbl.exe_path;
            string path = Path.Combine(root, "HDAssets", "UI_FRAME", "layouts", layout);
            if (System.IO.File.Exists(path))
            {
                Display.SetExternalImage("ui-frame", path, new Rectangle(0, 0, 320, 200), false);
            }
            else
            {
                Display.ClearExternalImage("ui-frame", false);
            }
        }
    }
}
