from sjvisualizer import Canvas
from sjvisualizer import DataHandler
from sjvisualizer import Date
from sjvisualizer import StaticText
from sjvisualizer import PieRace
import time
import json

def main(duration = 1.0, fps = 60, font_color=(225,225,225), background=(0,0,0)):
    number_of_frames = duration * fps * 60
    df = DataHandler.DataHandler(excel_file="Your/Directory/Here/market_share_prc_cons_assets_updated_9-8-2023-1.xlsx", number_of_frames=number_of_frames).df

    canvas = Canvas.canvas(bg=background) # create canvas object


    colors_costume={
        "Chase": (13, 94, 175), # Blue
        "Bank of America": (203, 13, 31), # Red
        "Wells Fargo": (255, 212, 8), #Yellow
        "Citibank": (21, 152, 195), # Blue-ish
        "PNC": (230, 100, 1), # Orange
        "Truist Bank": (93, 48, 153), #Purple
        "US Bank": (164, 164, 164), # Gray
        "Other Banks": (255, 229, 204), # Light Orange
    }
    # load colors
    with open("Your/Directory/Here/colors.json") as f:
        colors = json.load(f)
    
    
    
        # add pie chart
    pie = PieRace.pie_plot(canvas=canvas.canvas, df=df, x_pos=725, y_pos=250, height=750,
                                 width=350, colors=colors_costume, shift=150, unit="$T", display_percentages=True, display_label=True, font_color=font_color, back_ground_color=(0,0,0))
    canvas.add_sub_plot(pie)

    date = Date.date(canvas=canvas.canvas, df=df, time_indicator="month", width=0, height=65, x_pos=1550, y_pos=850,
                     font_color=font_color)
    canvas.add_sub_plot(date)

    title = StaticText.static_text(canvas=canvas.canvas, text="Percentage of Consolidated Assets per Bank", width=0, height=70, anchor="c",
                                   x_pos=950, y_pos=50, font_color=font_color)
    canvas.add_sub_plot(title)

    title = StaticText.static_text(canvas=canvas.canvas, text="Data Source: Federal Reserve", width=0, height=25, anchor="w",
                                   x_pos=250, y_pos=1000, font_color=font_color)
    canvas.add_sub_plot(title)

    title = StaticText.static_text(canvas=canvas.canvas, text="Made with: sjvisualizer", width=0, height=25, anchor="e",
                                   x_pos=1630, y_pos=1020, font_color=font_color)
    canvas.add_sub_plot(title)

    canvas.play(fps=fps)

main()
