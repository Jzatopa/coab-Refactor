using Classes;
using Logging;
using System.Collections.Generic;

namespace engine
{
    class ovr030
    {
        const string PictureLayer = "game-picture";
        const string PortraitHeadLayer = "portrait-head";
        const string PortraitBodyLayer = "portrait-body";
        const string BigpicLayer = "bigpic";

        sealed class HdAssetIdentity
        {
            public string Archive;
            public int Block;
            public int Frame;
        }

        static readonly Dictionary<DaxBlock, HdAssetIdentity> hdAssetIdentities =
            new Dictionary<DaxBlock, HdAssetIdentity>();
        static readonly HashSet<string> activeGameplayLayers = new HashSet<string>();
        static bool hdBigpicOverlayActive;
        static byte hdBigpicOverlayBlock = 0xff;
        static byte[] fadeOldColors = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 };
        static byte[] fadeNewColors = { 12, 12, 12, 12, 4, 5, 6, 7, 12, 12, 10, 12, 12, 12, 14, 12 };
        static byte[] transparentOldColors = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15 };
        static byte[] transparentNewColors = { 0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 0, 14, 15 };

        internal static void DrawMaybeOverlayed(DaxBlock dax_block, bool useOverlay, int rowY, int colX)// sub_7000A
        {
            if (dax_block != null)
            {
                HdAssetIdentity identity;
                hdAssetIdentities.TryGetValue(dax_block, out identity);

                if (identity == null)
                {
                    ClearLayer(PictureLayer, false);
                    ClearPortraitOverlays(false);
                }
                else if (identity.Archive.StartsWith("PIC"))
                {
                    ClearPortraitOverlays(false);
                }
                else
                {
                    ClearLayer(PictureLayer, false);
                }

                if (gbl.area_ptr.picture_fade > 0 || useOverlay == true)
                {
                    if (gbl.area_ptr.picture_fade > 0)
                    {
                        dax_block.Recolor(true, fadeNewColors, fadeOldColors);
                    }

                    seg040.OverlayBounded(dax_block, 0, 0, rowY - 1, colX - 1);
                    seg040.DrawOverlay();
                }
                else
                {
                    seg040.draw_picture(dax_block, rowY, colX, 0);
                }

                if (identity != null)
                {
                    string layer = null;
                    if (identity.Archive.StartsWith("PIC"))
                    {
                        layer = PictureLayer;
                    }
                    else if (identity.Archive.StartsWith("HEAD"))
                    {
                        layer = PortraitHeadLayer;
                    }
                    else if (identity.Archive.StartsWith("BODY"))
                    {
                        layer = PortraitBodyLayer;
                    }

                    if (layer != null)
                    {
                        HdAssetEntry hdEntry;
                        if (FindHdFrame(identity, out hdEntry))
                        {
                            Display.SetExternalImage(
                                layer,
                                hdEntry.Path,
                                new System.Drawing.Rectangle(
                                    colX * 8,
                                    rowY * 8,
                                    hdEntry.Width,
                                    hdEntry.Height),
                                true);
                            activeGameplayLayers.Add(layer);
                        }
                        else
                        {
                            ClearLayer(layer, false);
                        }
                    }
                }
            }
        }

        static bool FindHdFrame(HdAssetIdentity identity, out HdAssetEntry entry)
        {
            return HdAssetCatalog.TryGet(
                identity.Archive + ".DAX",
                identity.Block,
                identity.Frame,
                out entry);
        }

        static void RegisterHdFrame(DaxBlock block, string archive, int blockId, int frame)
        {
            if (block == null)
            {
                return;
            }

            hdAssetIdentities[block] = new HdAssetIdentity
            {
                Archive = archive,
                Block = blockId,
                Frame = frame
            };
        }


        internal static void load_pic_final(ref DaxArray daxArray, byte masked, byte block_id, string file_name)
        {
            if (file_name != gbl.lastDaxFile ||
                block_id != gbl.lastDaxBlockId)
            {
                if (block_id != 0xff)
                {
                    if (gbl.AnimationsOn)
                    {
                        ovr027.ClearPromptAreaNoUpdate();
                        seg041.displayString("Loading...Please Wait", 0, 10, 0x18, 0);
                    }

                    DaxArrayFreeDaxBlocks(daxArray);

                    gbl.lastDaxFile = file_name;
                    gbl.lastDaxBlockId = block_id;

                    bool is_pic_or_final = (file_name == "PIC" || file_name == "FINAL");

                    short uncompressed_size;
                    byte[] uncompressed_data;

                    seg042.load_decode_dax(out uncompressed_data, out uncompressed_size, block_id, file_name + gbl.game_area.ToString() + ".dax");

                    if (uncompressed_size == 0)
                    {
                        seg041.DisplayAndPause("PIC not found", 14);
                    }
                    else
                    {
                        int src_offset = 0;

                        daxArray.numFrames = uncompressed_data[src_offset];
                        src_offset++;
                        daxArray.curFrame = 1;

                        byte frames_count = 0; // kind of pointless...

                        if (gbl.AnimationsOn == false && is_pic_or_final == true)
                        {
                            daxArray.numFrames = 1;
                        }

                        byte[] first_frame_ega_layout = null;

                        for (int frame = 0; frame < daxArray.numFrames; frame++)
                        {
                            daxArray.frames[frame].delay = Sys.ArrayToInt(uncompressed_data, src_offset);
                            src_offset += 4;

                            short height = Sys.ArrayToShort(uncompressed_data, src_offset);
                            src_offset += 2;

                            short width = Sys.ArrayToShort(uncompressed_data, src_offset);
                            src_offset += 2;

                            frames_count++;

                            daxArray.frames[frame].picture = new DaxBlock(masked, 1, width, height);

                            DaxBlock dax_block = daxArray.frames[frame].picture;

                            dax_block.x_pos = Sys.ArrayToShort(uncompressed_data, src_offset);
                            src_offset += 2;

                            dax_block.y_pos = Sys.ArrayToShort(uncompressed_data, src_offset);
                            src_offset += 3;

                            System.Array.Copy(uncompressed_data, src_offset, dax_block.field_9, 0, 8);
                            src_offset += 8;

                            int ega_encoded_size = (daxArray.frames[frame].picture.bpp / 2) - 1;

                            if (is_pic_or_final == true)
                            {
                                if (frame == 0)
                                {
                                    first_frame_ega_layout = new byte[ega_encoded_size + 1];

                                    System.Array.Copy(uncompressed_data, src_offset, first_frame_ega_layout, 0, ega_encoded_size + 1);
                                }
                                else
                                {
                                    for (int i = 0; i < ega_encoded_size; i++)
                                    {
                                        byte b = first_frame_ega_layout[i];
                                        uncompressed_data[src_offset + i] ^= b;
                                    }
                                }
                            }

                            daxArray.frames[frame].picture.DaxToPicture(0, masked, src_offset, uncompressed_data);

                            if (file_name == "PIC")
                            {
                                RegisterHdFrame(
                                    daxArray.frames[frame].picture,
                                    "PIC" + gbl.game_area.ToString(),
                                    block_id,
                                    frame);
                            }

                            if ((masked & 1) > 0)
                            {
                                daxArray.frames[frame].picture.Recolor(false, transparentNewColors, transparentOldColors);
                            }

                            src_offset += ega_encoded_size + 1;
                        }

                        daxArray.numFrames = frames_count; // also pointless

                        uncompressed_data = null;
                        seg043.clear_keyboard();

                        if (gbl.AnimationsOn)
                        {
                            ovr027.ClearPromptAreaNoUpdate();
                        }
                    }
                }
            }
        }


        internal static void DaxArrayFreeDaxBlocks(DaxArray animation)
        {
            for (int index = 0; index < animation.numFrames; index++)
            {
                if (animation.frames[index].picture != null)
                {
                    hdAssetIdentities.Remove(animation.frames[index].picture);
                }
                animation.frames[index].picture = null;
                animation.frames[index].delay = 0;
            }

            animation.numFrames = 0;
            animation.curFrame = 0;

            gbl.lastDaxFile = string.Empty;
            gbl.lastDaxBlockId = 0x0FF;
        }


        internal static void head_body(byte body_id, byte head_id)
        {
            string text = gbl.game_area.ToString();

            if (System.Environment.GetEnvironmentVariable("COAB_HD_TRACE") == "1")
            {
                System.Console.Error.WriteLine(
                    "COAB_HD_HEAD_BODY area={0} head={1} body={2}",
                    text,
                    head_id,
                    body_id);
            }

            if (head_id != 0xff &&
                (gbl.current_head_id == 0xff || gbl.current_head_id != head_id))
            {
                if (gbl.headX_dax != null)
                {
                    hdAssetIdentities.Remove(gbl.headX_dax);
                }
                gbl.headX_dax = seg040.LoadDax(0, 0, head_id, "HEAD" + text);

                if (gbl.headX_dax == null)
                {
                    seg041.DisplayAndPause("head not found", 14);
                }

                gbl.current_head_id = head_id;
                RegisterHdFrame(gbl.headX_dax, "HEAD" + text, head_id, 0);
            }

            if (body_id != 0xff &&
                (gbl.current_body_id == 0xff || gbl.current_body_id != body_id))
            {
                if (gbl.bodyX_dax != null)
                {
                    hdAssetIdentities.Remove(gbl.bodyX_dax);
                }
                gbl.bodyX_dax = seg040.LoadDax(0, 0, body_id, "BODY" + text);
                if (gbl.bodyX_dax == null)
                {
                    seg041.DisplayAndPause("body not found", 14);
                }

                gbl.current_body_id = body_id;
                RegisterHdFrame(gbl.bodyX_dax, "BODY" + text, body_id, 0);
            }

            seg043.clear_keyboard();
        }


        internal static void draw_head_and_body(bool draw_body, byte rowY, byte colX) /* sub_706DC */
        {
            ClearLayer(PictureLayer, false);
            ClearPortraitOverlays(false);

            if (draw_body == true)
            {
                DrawMaybeOverlayed(gbl.headX_dax, false, rowY, colX);
                DrawMaybeOverlayed(gbl.bodyX_dax, false, rowY + 5, colX);
            }
            else
            {
                DrawMaybeOverlayed(gbl.headX_dax, false, rowY, colX);
            }
        }


        internal static void Show3DSprite(DaxArray arg_0, int sprite_index)
        {
            if (sprite_index < 1 || sprite_index > 3)
            {
                Logger.LogAndExit("Illegal range in Show3DSprite. {0}", sprite_index);
            }

            if (arg_0.frames[sprite_index - 1].picture != null)
            {
                DaxBlock block = arg_0.frames[sprite_index - 1].picture;
                seg040.OverlayBounded(arg_0.frames[sprite_index - 1].picture, 1, 0, block.y_pos + 3 - 1, block.x_pos + 3 - 1);
                seg040.DrawOverlay();
            }
        }


        internal static void load_bigpic(byte block_id) /* bigpic */
        {
            DaxArrayFreeDaxBlocks(gbl.byte_1D556);

            if (gbl.bigpic_block_id != block_id)
            {
                gbl.bigpic_dax = seg040.LoadDax(0, 0, block_id, "bigpic" + gbl.game_area.ToString());
                gbl.bigpic_block_id = block_id;
            }
        }


        internal static void draw_bigpic() /* sub_7087A */
        {
            seg037.DrawFrame_WildernessMap();
            seg040.draw_picture(gbl.bigpic_dax, 1, 1, 0);

            string archive = "BIGPIC" + gbl.game_area.ToString() + ".DAX";
            HdAssetEntry hdEntry;
            if (HdAssetCatalog.TryGet(archive, gbl.bigpic_block_id, 0, out hdEntry))
            {
                if (hdBigpicOverlayActive == false ||
                    hdBigpicOverlayBlock != gbl.bigpic_block_id)
                {
                    Display.SetExternalImage(
                        BigpicLayer,
                        hdEntry.Path,
                        new System.Drawing.Rectangle(8, 8, hdEntry.Width, hdEntry.Height),
                        true);
                    activeGameplayLayers.Add(BigpicLayer);
                    hdBigpicOverlayActive = true;
                    hdBigpicOverlayBlock = gbl.bigpic_block_id;
                }

                return;
            }

            ClearBigpicOverlay();
        }

        internal static void ClearBigpicOverlay()
        {
            ClearBigpicOverlay(true);
        }

        internal static void ClearBigpicOverlay(bool publishImmediately)
        {
            if (hdBigpicOverlayActive)
            {
                ClearLayer(BigpicLayer, publishImmediately);
                hdBigpicOverlayActive = false;
                hdBigpicOverlayBlock = 0xff;
            }
        }

        static void ClearLayer(string layer, bool publishImmediately)
        {
            if (activeGameplayLayers.Contains(layer))
            {
                Display.ClearExternalImage(layer, publishImmediately);
                activeGameplayLayers.Remove(layer);
            }
        }

        static void ClearPortraitOverlays(bool publishImmediately)
        {
            ClearLayer(PortraitHeadLayer, publishImmediately);
            ClearLayer(PortraitBodyLayer, publishImmediately);
        }

        internal static void ClearHdPictureOverlays(bool publishImmediately)
        {
            // Title images use the default presentation slot and manage their
            // own lifecycle in ovr002. Clear every gameplay layer first, then
            // publish at most once so no partial portrait/panel state leaks.
            bool hadActiveLayers = hdBigpicOverlayActive || activeGameplayLayers.Count > 0;
            ClearBigpicOverlay(false);
            ClearLayer(PictureLayer, false);
            ClearPortraitOverlays(false);
            if (publishImmediately && hadActiveLayers)
            {
                Display.ForceUpdate();
            }
        }

        static bool LayerIntersects(string key, System.Drawing.Rectangle logicalRect)
        {
            foreach (Display.ExternalImageLayer layer in Display.GetExternalImageSnapshot())
            {
                if (layer.Key == key)
                {
                    return logicalRect.IsEmpty ||
                        layer.LogicalRect.IsEmpty ||
                        layer.LogicalRect.IntersectsWith(logicalRect);
                }
            }

            return false;
        }

        internal static void ClearHdPictureOverlaysIntersecting(
            System.Drawing.Rectangle logicalRect,
            bool publishImmediately)
        {
            bool cleared = false;
            List<string> activeLayers = new List<string>(activeGameplayLayers);
            foreach (string layer in activeLayers)
            {
                if (LayerIntersects(layer, logicalRect))
                {
                    ClearLayer(layer, false);
                    cleared = true;

                    if (layer == BigpicLayer)
                    {
                        hdBigpicOverlayActive = false;
                        hdBigpicOverlayBlock = 0xff;
                    }
                }
            }

            if (publishImmediately && cleared)
            {
                // Publish once after all intersecting layers have retired so
                // a split portrait can never expose a partial intermediate.
                Display.ForceUpdate();
            }
        }
    }
}
