import requests
import obspython as obs


url = ""
refresh_rate = 10000



############################################ CUSTOM FUNCTIONS ###########################################

# main function
def requestWebhook():
    if(url != "" and url != None):
        result = requests.get(url)
        print(result)
        print(url)
    else:
        print('url is empty')
#



# CALLBACK FUNCTION FOR CHANGES IN SETTINGS

def callback(props, prop, settings):
    print('refreshing')

    u = obs.obs_data_get_string(settings, "url")
    r = obs.obs_data_get_int(settings, "refresh_rate")

    obs.obs_data_set_default_int(settings, "refresh_rate", r)
    obs.obs_data_set_default_string(settings, "url", u)

    print(u)
    print(r)

    #obs.timer_remove(requestWebhook)
    #obs.timer_add(requestWebhook, refresh_rate)

    return True
#



# EVENT HANDLER

def on_event(event):
    if event == obs.OBS_FRONTEND_EVENT_STREAMING_STARTING:
        print("Stream Started")
        obs.timer_add(requestWebhook, refresh_rate)

    elif event == obs.OBS_FRONTEND_EVENT_STREAMING_STOPPING:
        print("Stream Ended")
        obs.timer_remove(requestWebhook)

    else:
        print("Event: ", event)

    return True
#


############################################ OBS NATIVE API FUNCTIONS ###########################################


# load script when OBS starts
def script_load(settings):
    print('script loaded')
    url = obs.obs_data_get_string(settings, "url")
    refresh_rate = obs.obs_data_get_int(settings, "refresh_rate")
    obs.obs_frontend_add_event_callback(on_event);

    if(refresh_rate == 0):
        refresh_rate = 10000
    
    obs.obs_data_set_default_int(settings, "refresh_rate", refresh_rate);
#


# unload script when OBS closes
def script_unload():
    print('script unloaded')
    obs.timer_remove(requestWebhook)


# save settings
def script_save(settings, *args, **kwargs):
    print('script saved')
    obs.obs_data_set_default_string(settings, "url", url)
    obs.obs_data_set_default_int(settings, "refresh_rate", refresh_rate)
#

# create script properties to be shown in UI
def script_properties():
    props = obs.obs_properties_create()
    url = obs.obs_properties_add_text(props, "url", "Webhook URL", obs.OBS_TEXT_DEFAULT)
    refresh_rate = obs.obs_properties_add_int(props, "refresh_rate", "Refresh Rate (ms)", 10000, 60000, 100)

    refresh_button = obs.obs_properties_add_button(props, "button", "Refresh", obs.obs_property_set_modified_callback(url, callback))

    return props


# write out description to script window
def script_description():
    image = "https://media.tenor.com/zNmd9nLLAlQAAAAC/cat-gato.gif"

    description = """
        <style>
            .solid {
                border-top: 8px solid #bbb;
            }
        </style>
        

        <center>
            <h3>Song Request Webhooking Script</h3>

            <br><br>

            <img src="data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAGAAAABgCAQAAABIkb+zAAAA+ElEQVR42u3bsQ2DMBRFUTdMwQYMawl28BLMASNAReXa0kuXIgQi2yGx0b0tX+EfKXS2MURERER0mDpZzfL6dV6zrLq85RsNCvpnQYOa9PVHldCYSFCvUurT/vuhGEBI+BZkVVI2HjAVBZjiAb4ogI8HvPTp+dXzAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALSc7rNkz18OcKcLuez5ywGttsN1NrXZ81cDjFErp3W3zCq3Xyd+/geAd5Oxv/yN9wMAAAAAAAAAAAAAAADA7QDVH3yt/uhx9Ye/az9+X/0FiBtcQan+EtDzW6j3GhYRERHRzXsA036rQ5h+49UAAAAASUVORK5CYII=">

            <p>Vist <a href="api.grimfilerino.com">site</a> to get more help or to setup Song Request api connections</p>
            <p>
                You will find the webhook URL for your Song Request connection at 
                <a href="api.grimfilerino.com">api.grimfilerino.com</a> on the Song Request page
            </p>
        </center>
    """

    return description
#