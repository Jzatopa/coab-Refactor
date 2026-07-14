using Classes;
using System;
using System.Diagnostics;
using System.IO;

namespace engine
{
    public class seg044
    {
        static string[] sounds;
        static Process[] soundProcesses;
        static string soundDirectory;

        public static void SetSound(bool On)
        {
            gbl.soundType = On ? SoundType.PC : SoundType.None;
        }

        public static void SetPicture(bool On)
        {
            gbl.PicsOn = On;
        }

        public static void SetAnimation(bool On)
        {
            gbl.AnimationsOn = On;
        }

        internal static void PlaySound(Sound arg_0) /*sub_120E0*/
        {
            if (gbl.soundType != SoundType.PC)
            {
                return;
            }

            if (arg_0 == Sound.sound_0 || arg_0 == Sound.sound_FF)
            {
                StopAllSounds();
                return;
            }

            if (arg_0 >= Sound.sound_2 && arg_0 <= Sound.sound_e)
            {
                int sampleId = (int)arg_0 - 1;
                if (sounds[sampleId] != null)
                {
                    PlayExternalSound(sampleId, sounds[sampleId]);
                }
            }
        }

        static void StopAllSounds()
        {
            if (soundProcesses == null)
            {
                return;
            }

            for (int i = 0; i < soundProcesses.Length; i++)
            {
                Process process = soundProcesses[i];
                if (process != null && process.HasExited == false)
                {
                    try { process.Kill(); } catch (InvalidOperationException) { }
                }
                soundProcesses[i] = null;
            }
        }

        static void PlayExternalSound(int slot, string soundFile)
        {
            Process previous = soundProcesses[slot];
            if (previous != null && previous.HasExited == false)
            {
                try { previous.Kill(); } catch (InvalidOperationException) { }
            }

            try
            {
                ProcessStartInfo startInfo = new ProcessStartInfo();
                startInfo.FileName = "/usr/bin/ffplay";
                startInfo.Arguments = "-nodisp -autoexit -loglevel quiet -nostats -hide_banner \"" + soundFile + "\"";
                startInfo.UseShellExecute = false;
                startInfo.CreateNoWindow = true;
                soundProcesses[slot] = Process.Start(startInfo);
            }
            catch (Exception exception)
            {
                Logging.Logger.Log("Unable to play sound " + soundFile + ": " + exception.Message);
            }
        }

        static string ExtractSound(System.Resources.ResourceManager resources, string resourceName)
        {
            string output = Path.Combine(soundDirectory, resourceName + ".wav");
            if (System.IO.File.Exists(output) == false)
            {
                using (Stream input = resources.GetStream(resourceName))
                using (FileStream outputStream = System.IO.File.Create(output))
                {
                    input.CopyTo(outputStream);
                }
            }
            return output;
        }

        internal static void SoundInit()
        {
            var resources = new System.Resources.ResourceManager("Main.Resource", System.Reflection.Assembly.GetEntryAssembly());

            sounds = new string[13];
            soundProcesses = new Process[13];
            soundDirectory = Path.Combine(Path.GetTempPath(), "coab-refactor-sounds-" + Process.GetCurrentProcess().Id.ToString());
            Directory.CreateDirectory(soundDirectory);

            sounds[1] = ExtractSound(resources, "missle");
            sounds[2] = ExtractSound(resources, "magic_hit");
            sounds[4] = ExtractSound(resources, "death");
            sounds[5] = ExtractSound(resources, "sound_5");
            sounds[6] = ExtractSound(resources, "hit");
            sounds[8] = ExtractSound(resources, "miss");
            sounds[9] = ExtractSound(resources, "step");
            sounds[10] = ExtractSound(resources, "sound_10");
            sounds[12] = ExtractSound(resources, "start_sound");
        }
    }
}
