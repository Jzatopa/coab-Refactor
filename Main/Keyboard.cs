using System;
using System.Windows.Forms;

namespace Main
{
    /// <summary>
    /// Converts WinForms/Mono key values into the IBM BIOS keyboard words
    /// expected by engine.seg049.
    ///
    /// For extended keys such as arrows:
    ///   high byte = IBM BIOS scan code
    ///   low byte  = 0
    ///
    /// For ordinary character keys:
    ///   low byte  = ASCII character
    /// </summary>
    public class Keyboard
    {
        /// <summary>
        /// Preserves the original public method used by the COAB codebase.
        /// Returns 0 for keys that are not mapped.
        /// </summary>
        public static ushort KeyToIBMKey(Keys keyData)
        {
            ushort ibmKey;

            if (TryKeyToIBMKey(keyData, out ibmKey))
            {
                return ibmKey;
            }

            return 0;
        }

        /// <summary>
        /// Converts a WinForms/Mono key into the IBM keyboard value expected
        /// by engine.seg049. Modifier flags are removed before matching.
        /// </summary>
        public static bool TryKeyToIBMKey(
            Keys keyData,
            out ushort ibmKey)
        {
            Keys key = keyData & Keys.KeyCode;

            // Number row.
            if (key >= Keys.D0 && key <= Keys.D9)
            {
                ibmKey = (ushort)((key - Keys.D0) + '0');
                return true;
            }

            // Letter keys.
            if (key >= Keys.A && key <= Keys.Z)
            {
                ibmKey = (ushort)key;
                return true;
            }

            switch (key)
            {
                // Ordinary character/control keys.
                case Keys.Enter:
                    ibmKey = 0x1C0D;
                    return true;

                case Keys.Space:
                    ibmKey = 0x0020;
                    return true;

                case Keys.Back:
                    ibmKey = 0x0008;
                    return true;

                case Keys.Tab:
                    ibmKey = 0x0009;
                    return true;

                case Keys.Escape:
                    ibmKey = 0x001B;
                    return true;

                case Keys.OemMinus:
                case Keys.Subtract:
                    ibmKey = 0x002D;
                    return true;

                case Keys.Oemplus:
                case Keys.Add:
                    ibmKey = 0x002B;
                    return true;

                case Keys.Oemcomma:
                    ibmKey = 0x002C;
                    return true;

                case Keys.OemPeriod:
                    ibmKey = 0x002E;
                    return true;

                // IBM BIOS extended/navigation keys.
                // The low byte remains zero so seg049.READKEY()
                // returns zero first and the scan code next.

                case Keys.Home:
                case Keys.NumPad7:
                case Keys.OemOpenBrackets:
                    ibmKey = 0x4700;
                    return true;

                case Keys.Up:
                case Keys.NumPad8:
                    ibmKey = 0x4800;
                    return true;

                case Keys.PageUp:
                case Keys.NumPad9:
                    ibmKey = 0x4900;
                    return true;

                case Keys.Left:
                case Keys.NumPad4:
                    ibmKey = 0x4B00;
                    return true;

                case Keys.Clear:
                case Keys.NumPad5:
                    ibmKey = 0x4C00;
                    return true;

                case Keys.Right:
                case Keys.NumPad6:
                    ibmKey = 0x4D00;
                    return true;

                case Keys.End:
                case Keys.NumPad1:
                case Keys.OemCloseBrackets:
                    ibmKey = 0x4F00;
                    return true;

                case Keys.Down:
                case Keys.NumPad2:
                    ibmKey = 0x5000;
                    return true;

                case Keys.PageDown:
                case Keys.NumPad3:
                    ibmKey = 0x5100;
                    return true;

                case Keys.Insert:
                case Keys.NumPad0:
                    ibmKey = 0x5200;
                    return true;

                case Keys.Delete:
                case Keys.Decimal:
                    ibmKey = 0x5300;
                    return true;

                default:
                    ibmKey = 0;
                    return false;
            }
        }

        /// <summary>
        /// These keys can be consumed by WinForms/Mono as interface
        /// navigation commands. MainForm.ProcessCmdKey routes them
        /// directly to the game.
        /// </summary>
        public static bool IsWinFormsNavigationKey(Keys keyData)
        {
            Keys key = keyData & Keys.KeyCode;

            switch (key)
            {
                case Keys.Home:
                case Keys.Up:
                case Keys.PageUp:
                case Keys.Left:
                case Keys.Right:
                case Keys.End:
                case Keys.Down:
                case Keys.PageDown:
                case Keys.Insert:
                case Keys.Delete:
                    return true;

                default:
                    return false;
            }
        }
    }
}
