from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from plyer import gps
from jnius import autoclass, cast
from kivy.clock import Clock

class SafetyFeature(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.safety_button = Button(
            text='EMERGENCY',
            size_hint=(1, 0.2),
            background_color=(1, 0, 0, 1),  # Red color for emergency
            on_press=self.trigger_emergency
        )
        self.add_widget(self.safety_button)

    def trigger_emergency(self, instance):
        try:
            # Get Android Activity and Context
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            
            # Get emergency number
            TelephonyManager = autoclass('android.telephony.TelephonyManager')
            telephony = cast('android.telephony.TelephonyManager', 
                activity.getSystemService(activity.TELEPHONY_SERVICE))
            emergency_number = telephony.getEmergencyNumberList()[0].getNumber()

            # Intent to open emergency dialer
            Intent = autoclass('android.content.Intent')
            intent = Intent(Intent.ACTION_DIAL)
            intent.setData(autoclass('android.net.Uri').parse(f"tel:{emergency_number}"))
            intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
            
            # Start emergency call activity
            activity.startActivity(intent)

            # Get location and send to emergency contacts
            gps.configure(on_location=self.send_emergency_location)
            gps.start()

        except Exception as e:
            print(f"Error triggering emergency: {str(e)}")

    def send_emergency_location(self, **kwargs):
        try:
            # Stop GPS after getting location
            gps.stop()

            # Get location
            latitude = kwargs.get('lat', None)
            longitude = kwargs.get('lon', None)

            if latitude and longitude:
                # Create emergency SMS intent
                PythonActivity = autoclass('org.kivy.android.PythonActivity')
                Intent = autoclass('android.content.Intent')
                
                # Emergency contact (should be configurable by user)
                emergency_contact = "YOUR_EMERGENCY_CONTACT_NUMBER"
                
                # Create SMS intent
                sms_intent = Intent(Intent.ACTION_SEND)
                sms_intent.setType("text/plain")
                sms_intent.putExtra(Intent.EXTRA_TEXT, 
                    f"EMERGENCY! My current location: https://maps.google.com/?q={latitude},{longitude}")
                sms_intent.putExtra("address", emergency_contact)
                sms_intent.setFlags(Intent.FLAG_ACTIVITY_NEW_TASK)
                
                # Send SMS
                PythonActivity.mActivity.startActivity(sms_intent)

        except Exception as e:
            print(f"Error sending emergency location: {str(e)}") 