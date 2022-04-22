import streamlit as st
import streamlit.components.v1 as components
import streamlit as st
import pathlib
from PIL import Image

#p = pathlib.Path("skyline_barcelona.jpeg")
#img = Image.open(p)
st.image("https://github.com/Origamologo/Analisis-civitatis-Barcelona/blob/main/streamlit/skyline_barcelona.jpeg?raw=true")
original_title = '<p style="font-family:Vengeance Bold, sans-serif; color:#ff0262; font-size: 45px;">🌏 Civitatis marketing strategy 🌍</p>'
st.markdown(original_title, unsafe_allow_html=True)

#st.title("🌏 Civitatis' marketing strategy 🌍")

# Header/Subheader
#st.header("")
st.subheader("We will measure the effectiveness of civitatis' marketing strategy. To do so we will focus on Barcelona, one of the most competitive cities in the tourism industry, and we'll analize the performance of the most popular activity in civitatis' web page, the so called 'free tour', before and after the covid's lockdown.")

#audio_file = open("El_Turista_1999999.mp3","rb").read()
st.audio("https://github.com/Origamologo/Analisis-civitatis-Barcelona/blob/main/streamlit/El_Turista_1999999.mp3",format='audio/mp3')

status_1 = st.radio("Do you know what's civitatis?",("Yes","No"))

if status_1 == 'Yes':
	pass
else:
    st.info("Civitatis is an OTA (Online Tour Agency) focused on spanish speakers tourists, that was founded in 2008. In 2016 they opened their first phisical shop in the centre of Madrid, but their business is mainly based on the internet. They have pursued several marketing campaings including tv and radio advertisements, but the key of their success is that they've managed to settle their brand operating apart from the main rating platforms in tourism business like tripadvisor or yelp.\n\n The company has had a consistent growth untill the covid-19 crisis which forced the whole tourism industry to stop and restart from zero. In the post-covid casecenario, with the travels to and from foreing countries highly restricted, the brand presence among locals has been crucial for recovery.")

st.text("\n")
# Radio Buttons
status_2 = st.radio("Do you know what's a free tour?",("Yes","No"))

if status_2 == 'Yes':
	pass
else:
	st.info("A 'free tour' is a tour in which the tourist has to pay nothing to join\nthe activity, although he can tip the guide at the end of it. On the other hand,\nthe local guide must pay a fixed amount of money for each client that joins the tour\nto the OTA that provides the tourists. Taking on account that the risk for the\ncompanies is nearly zero, it's easy to figure out why this model, created by Chris\nSandemans in 2003, is nowadays followed by tons of companies (just type 'free tour'\non google and enjoy) and has become one of the main battle fields for walking tours\ncompanies.To check if the tourist who booked the activity actually showed up so they\ncan charge the guide (remember that it's free and you might feel in the mood for a\nbeer in stead of walking when the tour begins), civitatis ask the client for\na review. This is a very easy step for the client and he doesn't have to share any\ninformation if he doesn't want to, it works as a check in. If a tourist that was not\nreported by the local guide sends a review, the company will know that the guide is\ncheating... But for what matters to us, this means that the reviews in civitatis are\na trustful source of information regarding how many people joins the tours\nthey promote.")

st.error("For a correct visualization of the dashboard click on 'Deskopt mode'")
def main():    
    html_temp = """<div class='tableauPlaceholder' id='viz1650531297464' style='position: relative'><noscript><a href='#'><img alt='Portada ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;ci&#47;civitatis&#47;Portada&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='civitatis&#47;Portada' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;ci&#47;civitatis&#47;Portada&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='es-ES' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1650531297464');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='650px';vizElement.style.height='1027px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='650px';vizElement.style.height='1027px';} else { vizElement.style.width='100%';vizElement.style.height='727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>"""
    components.html(html_temp, height=900, width=800)
if __name__ == "__main__":    
	main()

st.markdown("Now let's see an historical view of the origin of the tourist that have join civitatis' free tour in Barcelona. You'll notice that most of them come from Spain and what happenned just after the lockdown is pretty obvious")

#HtmlFile = open("civitatis.html", 'r', encoding='utf-8')
#source_code = HtmlFile.read()
#components.html(source_code, height=900)
components.iframe("https://raw.githubusercontent.com/Origamologo/Analisis-civitatis-Barcelona/main/streamlit/civitatis.html", 
                height=900)

with open("civitatis.html", "rb") as file:

	btn = st.download_button(
	label="Download map",
	data=file,
	file_name="civitatis.html",
	mime='text/html'
)
 
st.sidebar.header("About")
st.sidebar.text("This work was developed while\nfollowing the Ironhack's bottcamp of\nData Analitycs")
st.sidebar.markdown("You can find the full code on [my github page](https://github.com/Origamologo/Analisis-civitatis-Barcelona)")