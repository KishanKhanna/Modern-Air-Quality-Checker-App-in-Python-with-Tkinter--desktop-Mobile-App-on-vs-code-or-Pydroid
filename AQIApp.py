import tkinter as tk
import requests
from PIL import Image, ImageDraw

class AQIApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Air Quality Check")
        self.master.geometry("400x600")
        self.master.configure(bg="#e0afe0")  # Set background color
        self.city_name = tk.StringVar()  # Variable to store the city name

        self.create_header()
        self.create_output_screen()
        self.create_input_area()
        self.create_submit_button()

    def create_header(self):
        header_frame = tk.Frame(self.master, bg="#e0afe0", height=90)
        header_frame.pack_propagate(False)
        header_frame.pack(fill=tk.X)

        header_label = tk.Label(header_frame, text="Air Quality Check", font=("Roboto", 20, "bold"), bg="#e0afe0")
        header_label.pack(expand=True)

    def create_output_screen(self):
        output_frame = tk.Frame(self.master, bg="#aeb1e8")
        output_frame.place(relx=0.05, rely=0.15, relwidth=0.9, relheight=0.35)

        # Set border round
        output_frame.config(bd=5, relief=tk.RIDGE)

        # Add heading label
        output_heading_label = tk.Label(output_frame, text="Output", font=("Roboto", 14, "bold"), bg="#aeb1e8")
        output_heading_label.pack(pady=5)

        self.output_label = tk.Label(output_frame, text="", font=("Roboto", 12), bg="#aeb1e8")
        self.output_label.pack(pady=5)

    def create_input_area(self):
        input_frame = tk.Frame(self.master, bg="#e0afe0")
        input_frame.place(relx=0.05, rely=0.55, relwidth=0.9, relheight=0.2)

        # Set border round
        input_frame.config(bd=5, relief=tk.RIDGE)

        # Create label for the text box
        label = tk.Label(input_frame, text="Enter city name:", font=("Roboto", 12), bg="#e0afe0")
        label.place(relx=0.05, rely=0.1)

        text_box = tk.Entry(input_frame, bg="light yellow", font=("Roboto", 12), bd=2, relief=tk.SOLID,
                            textvariable=self.city_name)
        text_box.place(relx=0.05, rely=0.5, relwidth=0.9, relheight=0.4)

    def create_submit_button(self):
        submit_button = tk.Button(self.master, text="Submit", font=("Roboto", 16), bg="#3ed136", bd=2,
                                  relief=tk.RIDGE, command=self.fetch_city_name)
        submit_button.place(relx=0.3, rely=0.8, relwidth=0.4, relheight=0.1)

        # Set border round for the button
        submit_button.config(bd=5, relief=tk.RIDGE)

        submit_button.bind("<Enter>", lambda event, button=submit_button: self.on_enter(button))
        submit_button.bind("<Leave>", lambda event, button=submit_button: self.on_leave(button))

    def fetch_city_name(self):
        city_name = self.city_name.get()
        print("City Name:", city_name)
        self.fetch_aqi(city_name)

    def fetch_aqi(self, city_name):
        if not city_name:
            self.output_label.config(text="Please enter a city name", fg="red")
            return

        # Replace API_KEY with your actual API key
        apikey = '7713f48b65c508d66a5a0855aa8cca5c79c58c9c'
        endpoint = 'https://api.waqi.info/feed/'

        try:
            # Send GET request to AQICN API
            response = requests.get(endpoint + city_name + '/', params={'token': apikey})

            # If the request is successful
            if response.status_code == 200:
                # Parse the response data
                data = response.json()
                air_quality = data['data']['aqi']
                city_name = city_name.capitalize()
                date_time = data['data']['time']['s']

                # Get the AQI remark
                aqi_remark = self.get_aqi_remark(air_quality)

                # Update context variable with air quality and error data
                context = {'air_quality': air_quality, 'city': city_name,"date_time": date_time, 'aqi_remark': aqi_remark}

                # Display AQI information on the UI
                self.display_aqi_info(context)
            else:
                self.output_label.config(text="Error fetching AQI data", fg="red")
        except Exception as e:
            print("Error fetching AQI:", e)
            self.output_label.config(text="Error fetching AQI data", fg="red")

    def get_aqi_remark(self, aqi_value):
        if aqi_value >= 0 and aqi_value <= 50:
            return "Good"
        elif aqi_value >= 51 and aqi_value <= 100:
            return "Moderate"
        elif aqi_value >= 101 and aqi_value <= 150:
            return "Unhealthy for Sensitive Groups"
        elif aqi_value >= 151 and aqi_value <= 200:
            return "Unhealthy"
        elif aqi_value >= 201 and aqi_value <= 300:
            return "Very Unhealthy"
        else:
            return "Hazardous"

    def display_aqi_info(self, context):
        # Clear existing AQI information
        self.output_label.config(text=f"City: {context['city']}\nDate & Time:\n {context['date_time']}\nAQI: {context['air_quality']}\n ({context['aqi_remark']})",
                                  fg="black")

    def on_enter(self, widget):
        widget.config(bg="#3d47cc")

    def on_leave(self, widget):
        widget.config(bg="#3ed136")


def main():
    root = tk.Tk()
    app = AQIApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
