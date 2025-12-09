import os
# Bibliothèque standard pour interagir avec le système d'exploitation, utilisée pour gérer les variables d'environnement. 2
import django
from fastmcp import FastMCP
#from mcp.server.fastmcp import FastMCP
# Importation de la classe FastMCP depuis le module fastmcp, utilisée pour créer un serveur MCP rapide.
from asgiref.sync import sync_to_async

# Importation de sync_to_async pour convertir des fonctions synchrones en asynchrones,compatible avec les ORM Django.
# Initialize Django environment
os.environ.setdefault("DJANGO_SETTINGS_MODULE","firstProject.settings")
django.setup()
# Importation des modèles Django après initialisation pour éviter des erreurs de configuration.

from ConferenceApp.models import Conference
from SessionApp.models import Session
# Create an MCP server 
mcp = FastMCP("Conference Assistant")
# Décorateur pour définir un outil MCP exécutable de manière asynchrone, rendant cette fonction accessible via le serveur MCP.
@mcp.tool()
async def list_conferences() -> str:
    """List all available conferences."""
    @sync_to_async # Ce décorateur permet d'appeler des méthodes synchrones de l'ORM Django dans un contexte asynchrone, évitant les blocages.
    def _get_conferences():
    # Fonction interne synchrone pour récupérer la liste des conférences depuis la base de données.
        return list(Conference.objects.all())

    conferences = await _get_conferences()
    # Appel asynchrone à la fonction interne pour obtenir les conférences, en attendant le résultat.
    if not conferences:
        return "No conferences found."
    return "\n".join([f"- {c.name} ({c.start_date} to {c.end_date})" for c in conferences])
# Construit une chaîne formatée avec le nom et les dates de chaque conférence, séparées par des sauts de ligne.

@mcp.tool()
async def get_conference_details(name: str) -> str:
"""Get details of a specific conference by name."""
    @sync_to_async
        def _get_conference():
        try:
            return Conference.objects.get(name__icontains=name)
        except Conference.DoesNotExist:
            return None
        except Conference.MultipleObjectsReturned:
            return "MULTIPLE"

    conference = await _get_conference()
    if conference == "MULTIPLE":
        return f"Multiple conferences found matching '{name}'. Please be more specific."
    if not conference:
    return f"Conference '{name}' not found."
    return (
        f"Name: {conference.name}\n"
        f"Theme: {conference.get_theme_display()}\n"
        f"Location: {conference.location}\n"
        f"Dates: {conference.start_date} to {conference.end_date}\n"
        f"Description: {conference.description}"
    )

# Lancement if name always last thing in server
if __name__ == "__main__":
    mcp.run(transport="stdio")