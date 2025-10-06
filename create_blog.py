from app import create_app, db
from config import Config

from app.models import BlogPost 

app = create_app(config_class=Config)

with app.app_context():
    u = BlogPost(title="US democratic backsliding and a warning against Chat Control",
                 subtitle="How large scale surveillance and AI was quickly turned against expression in the country that prides itself on freedom of speech.",
                 body="""
In March 2025, a French scientist was [denied entry](https://www.theguardian.com/us-news/2025/mar/19/trump-musk-french-scientist-detained) to the US, after the messages on his phone were searched and criticism of the Trump administration was found by border agents. Google and Meta are [handing over](https://theintercept.com/2025/09/16/google-facebook-subpoena-ice-students-gaza/) social media, email and location data to immigration officers of protesters against Israel’s war on Gaza. Both [US colleges](https://pulitzercenter.org/stories/tracked-how-colleges-use-ai-monitor-student-protests) and [US authorities](https://www.amnesty.org/en/latest/news/2025/08/usa-global-tech-made-by-palantir-and-babel-street-pose-surveillance-threats-to-pro-palestine-student-protestors-migrants/) are using invasive AI-powered technologies to track activists and migrants, making use of large combined databases of scraped data.

Against this background, it is chilling that the Danish EU Presidency is pushing for the adoption of the so-called Chat Control Regulation ([Regulation to Prevent and Combat Child Sexual Abuse](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:52022PC0209)). A new vote of Member States on the proposal would advance the contentious legislation, after it had been dormant in the Council since 2024.

Much of the mass-surveillance, as employed in the US would be a lot less effective in the EU. Companies such as Babel Street and Palantir rely on large amounts of both private databases and scraped public data. The EU Charter of Fundamental Rights and more detailed legislation, such as the GDPR, have prevented such large interconnected databases in Europe.

However, none of these protections would protect us from government overreach, if Chat Control would be implemented in the EU. While the technical implementation and feasibility is seemingly treated as a detail to be hashed out at a later date, every realistic measure would result in severe degradation of the security of online systems and large scale violation of the privacy of all EU citizens.

While the Commission [presented](https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:52022SC0209&from=EN) 9 potential technical solutions, these boil down to two approaches: allowing all messages by all EU citizens to be screened, allowing targeted screening of encrypted messages, or a combination of these two. The difference lies in who has access, how the information is screened and where it is screened.

Democracies in the EU are also backsliding. What I have to say now is not illegal or persecuted anywhere. But neither was this the case for students protesting genocide in Gaza or visitors criticising the government in the US just a year ago. With an example of how quick guardrails and protections erode under anti-democratic governments, we should not even consider the possibility of undermining the privacy and cybersecurity of 450 million EU citizens.
                 """,
                 image="img/blog/us_chat_control.png",
                 thumbnail="img/blog/thumb_us_chat_control.png",
                 extract="The use of data access, databases and AI to limit free speech and other rights in the US during the second Trump administration should serve as a warning against the EU's proposed Chat Control.",
                 slug="US-democratic-backsliding-and-a-warning-against-Chat-Control")
    db.session.add(u)
    db.session.commit()
