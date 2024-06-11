import argparse
import os
from datetime import datetime

import agentops
from dotenv import load_dotenv
from pathvalidate import sanitize_filename

from crew import generate_article

EXISTING_ARTICLES = [
    {
        "title": "Copier le presse-papiers avec JavaScript",
        "url": "https://tim-tek.com/2024/05/15/copier-le-presse-papiers-avec-javascript/",
        "summary": "Cet article explique comment implémenter la fonctionnalité de copie dans le presse-papiers en JavaScript. Il détaille deux méthodes principales : document.execCommand('copy'), compatible avec tous les navigateurs, et l'API Clipboard moderne, plus simple mais supportée uniquement par les navigateurs récents. L'article souligne aussi l'importance de la sécurité et de la confidentialité lors de l'utilisation de cette fonctionnalité.",
    },
    {
        "title": "Les évolutions clés de React en 2024 : impact et opportunités",
        "url": "https://tim-tek.com/2024/04/17/les-evolutions-cles-de-react-en-2024-impact-et-opportunites/",
        "summary": "Cet article explore les dernières évolutions de React en 2024, en mettant l'accent sur les nouvelles fonctionnalités et leurs impacts sur le développement d'applications. Il discute des opportunités offertes par ces changements pour les développeurs, notamment en termes de performance, de facilité d'utilisation et de capacités avancées pour la création d'interfaces utilisateur interactives.",
    },
    {
        "title": "Focus métier : développeur C++",
        "url": "https://tim-tek.com/2023/09/19/focus-metier-dev-c/",
        "summary": "Cet article offre un aperçu approfondi du métier de développeur C++. Il aborde les compétences nécessaires, les responsabilités typiques, et les perspectives de carrière dans ce domaine. L'article met également en lumière les défis et les avantages spécifiques du travail avec le langage C++, ainsi que les secteurs où cette expertise est particulièrement recherchée.",
    },
    {
        "title": "Timtek fête ses 3 ans d’existence",
        "url": "https://tim-tek.com/2022/11/16/anniversaire-timtek/",
        "summary": "À l'occasion de son troisième anniversaire, Timtek célèbre ses succès et partage ses projets futurs. L'article revient sur les réalisations majeures de l'entreprise depuis sa création, les défis surmontés et les collaborations fructueuses. Il met en lumière la croissance de Timtek et ses ambitions pour les années à venir.",
    },
    {
        "title": "Top 10 des langages de programmation en 2021",
        "url": "https://tim-tek.com/2021/09/14/top-10-langages-programmation-2021/",
        "summary": "Cet article présente les dix langages de programmation les plus populaires en 2021. Il analyse les tendances et les raisons de la popularité de chaque langage, en tenant compte des évolutions technologiques et des besoins du marché. Les avantages et les utilisations principales de chaque langage sont également discutés, offrant un guide utile pour les développeurs en quête de nouveaux horizons.",
    },
    {
        "title": "Le cliché du développeur insociable",
        "url": "https://tim-tek.com/2021/09/09/cliche-le-developpeur-est-insociable/",
        "summary": "Cet article démystifie le stéréotype du développeur insociable. Il examine les origines de ce cliché et propose une vision plus nuancée de la réalité. L'article met en avant les compétences sociales et de communication souvent nécessaires dans le métier de développeur, et montre comment la collaboration et l'interaction sont au cœur du développement logiciel moderne.",
    },
    {
        "title": "Timtek fait la fête",
        "url": "https://tim-tek.com/2021/06/29/la-timtek-fait-la-fete/",
        "summary": "Cet article décrit une journée de fête organisée par Timtek pour ses employés. Il relate les activités et les moments forts de l'événement, soulignant l'importance de la convivialité et du renforcement des liens au sein de l'équipe. La fête est présentée comme une occasion de célébrer les réussites collectives et de motiver les employés.",
    },
    {
        "title": "C’est quoi un POC ?",
        "url": "https://tim-tek.com/2020/11/29/cest-quoi-un-poc/",
        "summary": "L'article explique le concept de Proof of Concept (POC) dans le développement logiciel. Il détaille les objectifs et les étapes clés de la réalisation d'un POC, ainsi que les critères de succès. En illustrant avec des exemples concrets, il montre comment un POC peut valider des idées et des technologies avant de passer à des développements plus poussés.",
    },
    {
        "title": "CSS, la relève de Bootstrap ?",
        "url": "https://tim-tek.com/2020/10/20/css-la-releve-de-bootstrap/",
        "summary": "Cet article compare CSS et Bootstrap, en analysant les avantages et les inconvénients de chacun. Il discute des évolutions récentes de CSS, qui le rendent de plus en plus compétitif face à Bootstrap. L'article examine comment les nouvelles fonctionnalités de CSS peuvent simplifier le développement de sites web réactifs et stylisés sans recourir à des frameworks externes.",
    },
]


def get_arguments():
    """Parse and return command-line arguments."""
    parser = argparse.ArgumentParser(
        description="Generate and save an article based on a given topic."
    )
    parser.add_argument("topic", type=str, help="The topic for the article.")
    parser.add_argument(
        "-L",
        "--language",
        type=str,
        default="French",
        help="The language of the article (default: French).",
    )
    return parser.parse_args()


def sanitize_title(title: str, topic: str) -> str:
    """Sanitize the title of the article."""
    sanitized_title = title.split("\n")[0].strip().strip("#").strip()
    if not sanitized_title:
        sanitized_title = topic
    return sanitize_filename(sanitized_title).replace(" ", "_")


def save_article(article: str, sanitized_title: str) -> str:
    """Save the article to a file and return the file path."""
    filename = f"{datetime.now().strftime('%Y_%m_%d_%H_%M_%S')}_{sanitized_title}.md"
    path = os.path.join("posts", filename)
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        f.write(article)

    return path


def main():
    """Main function to generate and save the article."""
    load_dotenv()
    args = get_arguments()

    agentops.init()

    try:
        article = generate_article(
            topic=args.topic,
            language=args.language,
            existing_articles=EXISTING_ARTICLES,
        )
        print(article)

        title = sanitize_title(article, args.topic)
        path = save_article(article, title)

        print(f"Article saved to {path}")

    except KeyboardInterrupt:
        agentops.end_session("Fail", end_state_reason="User Interrupted")
        print("Operation cancelled by user.")
    except Exception as e:
        print(f"Error generating article: {e}")
        agentops.end_session("Fail", end_state_reason=str(e))
    else:
        agentops.end_session("Success")


if __name__ == "__main__":
    # Enable Langchain tracking
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    main()
