#!/usr/bin/python3

# Do not edit this thing unless you know what youre doing
# - AA07

import requests, sys, mwclient

# Holder class so we can do element.filename and element.pagename
class WikiPage:
    def __init__(self, _filename, _pagename):
        self.filename = _filename
        self.pagename = _pagename

    def formatname(self):
        return "{}/{}".format(self.filename, self.pagename)

# Function to compare a local copy against the remote pages. Returns True if there is a difference
def compare_changes(wikipage):
    check_url = "{}?action=parse&page={}&prop=wikitext&formatversion=2&format=json".format(wiki_api_url, wikipage.pagename)
    returned_data = requests.get(check_url).json()
    remote_content = returned_data["parse"]["wikitext"]
    f = open(wikipage.filename, "r", encoding="utf8")
    local_content = f.read()
    f.close()

    # Trim both to remove whitespace that could create dirty diffs
    local_content = local_content.strip()
    remote_content = remote_content.strip()

    # And compare
    if local_content == remote_content:
        return False        
    else:
        return True


# Wiki API key
if len(sys.argv) > 1:
    wiki_api_key = sys.argv[1]
else:
    print("Args not suppplied")
    exit()

# Base wiki API url
wiki_api_url = "https://paradisestation.org/wiki/api.php"

# List of all wiki pages and their corresponding files
wiki_documents = [
    WikiPage("aa_debug.wiki", "User:AffectedArc07/AA_Debug"),
    #WikiPage("sop_command.wiki", "Standard_Operating_Procedure_(Command)"),
    #WikiPage("sop_engineering.wiki", "Standard_Operating_Procedure_(Engineering)"),
    #WikiPage("sop_legal.wiki", "Legal_Standard_Operating_Procedure"),
    #WikiPage("sop_main.wiki", "Standard_Operating_Procedure"),
    #WikiPage("sop_medical.wiki", "Standard_Operating_Procedure_(Medical)"),
    #WikiPage("sop_science.wiki", "Standard_Operating_Procedure_(Science)"),
    #WikiPage("sop_security.wiki", "Standard_Operating_Procedure_(Security)"),
    #WikiPage("sop_service.wiki", "Standard_Operating_Procedure_(Service)"),
    #WikiPage("sop_supply.wiki", "Standard_Operating_Procedure_(Supply)"),
]

if wiki_api_key is not None:
    print("API key is set")

print("Checking existing pages")
for wiki_page in wiki_documents:
    if compare_changes(wiki_page):
        # Report change
        print("Changes were made to {}. Updating the wiki...".format(wiki_page.formatname()))
        # Perform a wiki update
        site = mwclient.Site('www.paradisestation.org', path='/wiki/')
        site.login('ParadiseWikibot', wiki_api_key)
        page = site.Pages[wiki_page.pagename]
        # Get new text
        f = open(wiki_page.filename, "r", encoding="utf8")
        local_content = f.read()
        f.close()

        # Trim it down
        local_content = local_content.strip()

        # Save the page - todo - include commit hash and the like
        page.edit(text=local_content, summary="Automatic update. Check https://github.com/ParadiseSS13/WikiDocs for details", tags="Github")
    else:
        # Report no change
        print("No change to {}".format(wiki_page.formatname()))

exit(0)
