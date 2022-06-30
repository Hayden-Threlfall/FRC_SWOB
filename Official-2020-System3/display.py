from typing_extensions import Self
from numpy import inner
import pandas as pd
import math, os
import statistics


from htmls import * #if you name it html (no s) one of the imports breaks the code




MATCH_FP = "data/match_scouting.csv"
PIT_FP = "data/pit_scouting.csv"
REPORTS_DIR = "reports/"

def make_list(title, items, parent):
    div = DivElement(parent=parent, children=PElement(children=title), _class="list")

    ul = UlElement(parent=div)
    for item in items:
        li = LiElement(parent=ul)
        li.append_child(item)

    return div


def make_answer(title, answer, parent):
    div = DivElement(parent=parent, _class="answer")
    div.append_child(PElement(children=title, _class="q"))
    _class = "a"
    if isinstance(answer, str):
        if answer.lower().startswith("yes"):
            _class += " green"
        elif answer.lower().startswith("no"):
            _class += " red"
    div.append_child(PElement(children=answer, _class=_class))
    return div


def generate_report(team_number):

    # Get specified team's data

    pit_scouting = all_pit_scouting[all_pit_scouting["Team you're scouting? (number)"] == team_number]
    match_scouting = all_match_scouting[all_match_scouting["What team are you scouting?"] == team_number]

    pit_scouting_h = list(pit_scouting)
    pit_scouting = pit_scouting.values
    match_scouting_h = list(match_scouting)
    match_scouting = match_scouting.values

    team_name = pit_scouting[0][pit_scouting_h.index("Team you're scouting? (name)")]

    html = HTMLElement("html", children="""<head> <link rel="stylesheet" type="text/css" href="style.css"> </head>""")
    body = HTMLElement("body", parent=html)

    # Display pit scouting

    pit_section = SectionElement(parent=body, _class="pit")

    H1Element(parent=pit_section, children="{} <span>|</span> {}".format(team_name, team_number))

    DivElement(parent=pit_section,children='<img width="400" height="300" src=\"images/{}.jpg\" alt="No image found for team"></img>'.format(team_number))

    lists = {}
    answers = {}
   

    for i, h in enumerate(pit_scouting_h):
        val = pit_scouting[:, i][0]
        if i <= 3:
            continue
        if h in ["Where can the shooter reach?", "Does the robot extend out of it's frame, and can it go back in?"]:
            items = val.split(", ")
            lists[h] = items
        elif h in ["Team you're scouting? (name)", "Team you're scouting? (number)","Comments"]:
            pass
        else:
            answers[h] = val

    lists_div = DivElement(parent=pit_section)
    for h in lists:
        make_list(h, lists[h], parent=lists_div)

    answers_div = DivElement(parent=pit_section)
    for h in answers:
        make_answer(h, answers[h], parent=answers_div)

    # Display match scouting

    matches_h = match_scouting_h[3:-1]
    matches = match_scouting[:, 3:-1]

    

    matches_played = len(matches)

    match_section = SectionElement(parent=body,  _class="match")

    # Matches played
    div = DivElement(parent=match_section)
    PElement(children="Matches played: {}".format(matches_played), parent=div)

    # Match table
    if matches_played > 0:
        table = TableElement(parent=match_section, _class="match_table")

        means = TRElement(parent=table)
        modes = TRElement(parent=table)
        medians = TRElement(parent=table)
        ranges = TRElement(parent=table)
        for i, h in enumerate(matches_h):
            if 5 <= i <= 10:
                nums = []
                for n in matches[:, i]:
                    if isinstance(n, str):
                        last = n.split(",")[-1]
                        print(i)
                        nums.append(int(last))
                    else:
                        if math.isnan(n):
                            nums.append(0)
                        else:
                            nums.append(n)
                avg = sum(nums)/len(nums)
                mode = max(set(nums), key=nums.count)
                median = statistics.median(nums)
                rang = max(nums) - min(nums)
                means.add_td(avg)
                modes.add_td(mode)
                medians.add_td(median)
                ranges.add_td(rang)
            elif i == 4:
                means.add_td("MEAN")
                modes.add_td("MODE")
                medians.add_td("MEDIAN")
                ranges.add_td("RANGE")
            elif h == "Any breakdowns?":
                good = 0
                count = 0
                for s in matches[:, i]:
                    count += 1
                    if s == "Yes":
                        good += 1
                ranges.add_td("Total breakdowns: {} / {}".format(good, count))
            elif h == "Did they play any defense?":
                good = 0
                count = 0
                for s in matches[:, i]:
                    count += 1
                    if s == "Yes":
                        good += 1
                ranges.add_td("Times defended: {} / {}".format(good, count))
            elif h == "Did they climb?":
                unique = set(matches[:, i])
                string = ", ".join(unique)
            elif h == "How good was the driver?":
                continue
            else:
                means.add_td()
                modes.add_td()
                medians.add_td()
                ranges.add_td()

        tr = TRElement(parent=table)
        for header in matches_h:
            if header == 'How good was the driver?':
                continue
            THElement(children=header, parent=tr)
        THElement(children="Total balls", parent=tr
                  )
        

        total_total_balls = 0
        for row in matches:
            tr = TRElement(parent=table)
            total_balls = 0
            for i, col in enumerate(row):
                if isinstance(col, float) and not math.isnan(col):
                    if int(col) == col:
                        col = int(col)
                if 5 <= i <= 10:
                    if not math.isnan(col):
                        if i % 2 == 0:
                            total_balls += col
                        else:
                            total_balls += col
                if i != 17:
                    TDElement(children=col, parent=tr)

            TDElement(children=total_balls, parent=tr)
            total_total_balls += total_balls

        totals = TRElement(parent=table)
        for i, h in enumerate(matches_h):
            if 5 <= i <= 10:
                total = 0
                for n in matches[:, i]:
                    if isinstance(n, str):
                        last = n.split(",")[-1]
                        total += int(last)
                    else:
                        if not math.isnan(n):
                            total += n
                totals.add_td(total)
            elif i == 4:
                totals.add_td("TOTAL")
            elif h == 'How good was the driver?' or i == 17:
                continue
            else:
                totals.add_td()
        totals.add_td("{} (avg {})".format(total_total_balls, total_total_balls/matches_played))

        # Comments
       

    with open(os.path.join(REPORTS_DIR, "report{}.html".format(team_number)), "w") as f:
        f.write(str(html))


def make_index():
    html = HTMLElement("html", children="""<head> <link rel="stylesheet" type="text/css" href="style.css"> </head>""")
    body = HTMLElement("body", parent=html, children="<h1>REPORT LIST</h1>")

    report_list = UlElement(parent=body, _class="report-list")
    files = [fn for fn in os.listdir(REPORTS_DIR) if fn.endswith(".html") and fn.startswith("report")]
    files = {fn: int(fn.strip(".html").strip("report")) for fn in files}
    for fp in sorted(files, key=files.get):
        href = fp
        num = files[fp]
        LiElement(parent=report_list, children="<a href='{}'>Report {}</a>".format(href, num))

    with open(os.path.join(REPORTS_DIR, "index.html"), "w") as f:
        f.write(str(html))


all_match_scouting = pd.read_csv(MATCH_FP)
all_pit_scouting = pd.read_csv(PIT_FP)

for team_number in all_pit_scouting["Team you're scouting? (number)"]:
    if not math.isnan(team_number):
        team_number = int(team_number)
        generate_report(team_number)

make_index()
