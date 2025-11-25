import gradio as gr
import libtorrent as lt
import urllib.parse
import os

def torrent_to_magent(filepaths):
    magnet_links = []
    for filepath in filepaths:
        """Convert a .torrent file to a magnet link with all metadata"""
        info = lt.torrent_info(filepath)
        
        # Start with info hash (required)
        magnet_link = f"magnet:?xt=urn:btih:{info.info_hash()}"
        
        # Add display name
        if info.name():
            magnet_link += f"&dn={urllib.parse.quote(info.name())}"
        
        # Add trackers
        for tracker in info.trackers():
            magnet_link += f"&tr={urllib.parse.quote(tracker.url)}"
        
        # Add web seeds
        for seed in info.web_seeds():
            magnet_link += f"&ws={urllib.parse.quote(seed.url)}"
        
        magnet_links.append(magnet_link)
    
    return (os.linesep).join(magnet_links)


demo = gr.Interface(
    fn=torrent_to_magent,
    inputs=gr.File(label="Upload .torrent file", file_count="multiple", file_types=[".torrent"]),
    outputs=[gr.Textbox(label="Magnet Link", show_copy_button=True, lines=5, max_lines=10, interactive=True,)],
    title="Torrent to Magnet Link Converter",
    flagging_mode="never",
)

demo.launch()
