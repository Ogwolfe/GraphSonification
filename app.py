from shiny import App, render, ui, reactive
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import io
import base64
import os
from pathlib import Path
from sonify_graph import transform_notes, create_melody, sig, beat

# Define the path to your audio file

current_dir = Path(__file__).parent

app_ui = ui.page_fluid(
    ui.input_file("file1", "Choose CSV File", accept=[".csv"]),
    ui.output_ui("column_selector"),
    ui.output_plot("density_plot"),
    ui.output_ui("play_button"),
    ui.tags.audio(id="audio_player", style="display: none;"),
    ui.tags.script("""
    var audio = document.getElementById('audio_player');
    Shiny.addCustomMessageHandler('play_audio', function(message) {
        audio.src = message.src;
        audio.play();
    });
    """)
)

def server(input, output, session):
    data = reactive.Value(None)
    graph_created = reactive.Value(False)
    audio_file = reactive.Value(None)

    
    @reactive.Effect
    @reactive.event(input.file1)
    def _():
        file = input.file1()
        if file is not None and file[0]['type'] == 'text/csv':
            data.set(pd.read_csv(file[0]['datapath']))
        else:
            data.set(None)

    @output
    @render.ui
    def column_selector():
        if data() is not None:
            return ui.input_select("column", "Select Column", choices=data().select_dtypes(include=['int64', 'float64']).columns.tolist())
        return ui.div()

    @output
    @render.plot
    def density_plot():
        if data() is not None and input.column():
            df = data.get()
            plt.figure(figsize=(10, 6))
            ax = sns.kdeplot(data=df, x=input.column(), fill=True, color='black', alpha=0.1)
            sns.kdeplot(x=df[input.column()], fill=False, color='red', ax=ax)
            plt.title(f'KDE Plot of {input.column()}')
            plt.xlabel(input.column())
            plt.ylabel('Density')
            graph_created.set(True)

            x_values, y_values = ax.lines[0].get_data() 
            notes = []
            for i in range(20, 200, 5):
                notes.append(y_values[i])

            q = transform_notes(notes)
            melody = create_melody(q)
            S = sig(melody, beat)

            S.export("basic-sidebar/sonified_graph.mp3")

            return ax
    
    @output
    @render.ui
    def play_button():
        if graph_created.get():
            return ui.input_action_button("play_melody", "Play graph audio")
        else:
            return ui.div()
        
    @reactive.Effect
    @reactive.event(input.play_melody)
    async def play_mp3():
        #audio_url = f"/{audio_file.get()}"
        await session.send_custom_message('play_audio', {'src': '/sonified_graph.mp3'})

app = App(app_ui, server, static_assets=str(current_dir))
