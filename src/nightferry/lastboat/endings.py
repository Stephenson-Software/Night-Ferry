# @author Daniel McCoy Stephenson
"""The last page of the last night boat.

The same contract as nightferry.endings: each ending says what happened,
where the captain was going, what the player did, and what it cost whom -
everyone aboard, by name, in a sentence of their own - and then what it was.
The first crossing is part of it: what was done in October is remembered
here, in the costs and in a paragraph for the people who are not aboard.
"""

from nightferry import endings as firstEndings
from nightferry import flags
from nightferry.lastboat import carried

ON_WHICH_DAYS = "on_which_days"
THE_COLUMN = "the_column"
OVER_THE_SIDE = "over_the_side"
KEPT_FROM_THE_RECORD = "kept_from_the_record"

ENDINGS = (ON_WHICH_DAYS, THE_COLUMN, OVER_THE_SIDE, KEPT_FROM_THE_RECORD)

NAMES = {
    ON_WHICH_DAYS: "on which days",
    THE_COLUMN: "the column",
    OVER_THE_SIDE: "over the side",
    KEPT_FROM_THE_RECORD: "kept from the record",
}


def name(state):
    return NAMES.get(state.ending, "Brekka")


def atBrekka(state):
    """Which ending six o'clock comes to: where the books went, and - if
    they went over the side - whether Hanne has Oskar's column instead."""
    if state.flags.get(flags.BOOKS_TO_HANNE):
        return ON_WHICH_DAYS
    if state.flags.get(flags.BOOKS_OVERBOARD):
        if state.flags.get(flags.COLUMN_TO_HANNE):
            return THE_COLUMN
        return OVER_THE_SIDE
    return KEPT_FROM_THE_RECORD


def text(state):
    builders = {
        ON_WHICH_DAYS: _onWhichDays,
        THE_COLUMN: _theColumn,
        OVER_THE_SIDE: _overTheSide,
        KEPT_FROM_THE_RECORD: _keptFromTheRecord,
    }
    opening, hanne, ingrid, close = builders.get(state.ending, _keptFromTheRecord)(
        state
    )
    return "\n\n".join(
        [opening, _whereSheWasGoing(state), _whatYouDid(state), "WHAT IT COST."]
        + [hanne, ingrid]
        + _everyoneElse(state)
        + [_fromOctober(state), close]
    )


# --- shared paragraphs --------------------------------------------------------
OCTOBER = {
    firstEndings.OFF_THE_LIGHT: "In October, from this ship's stern, Hanne and "
    "Ingrid put Maren into the water off the Halde light.",
    firstEndings.BESIDE_ARNE: "In October Maren was buried beside Arne, and "
    "Hanne knew why she had asked not to be.",
    firstEndings.AT_THE_DOOR: "In October it came out in a corridor at four in "
    "the morning, because nobody else had said it.",
    firstEndings.KEPT_CROSSING: "In October you kept the captain's secret, and "
    "Hanne went ashore not knowing.",
}


def _whereSheWasGoing(state):
    return (
        "WHERE THE CAPTAIN WAS GOING. Away. Ingrid Halvard sold Harbour House and "
        "Maren's piano, booked a single south, and crossed on the last night boat "
        "as a passenger in cabin 6, where for nineteen years of Fridays she had "
        "never once spent a whole night. In a box marked BALLAST she carried the "
        "crossword books from six's drawer - both their hands, every Friday, and "
        "in the margins, in Maren's print, 'Happy. - M.' - meaning to put them "
        "over the side at five, the hour she always went back up. Maren had asked "
        "her to tell Hanne she was happy, and on which days. "
        + OCTOBER.get(carried.octoberEnding(state), "")
    ).rstrip()


def _whatYouDid(state):
    f = state.flags
    did = []
    if f.get(flags.INGRID_TOLD_YOU_TONIGHT) and not f.get(flags.AT_THE_STERN):
        did.append("you found out where the captain was going before five")
    if f.get(flags.OPENED_SIX_AGAIN):
        did.append("you opened six while she was on the bridge")
    if f.get(flags.READ_A_BOOK):
        did.append("you untied the string and read one of the books")
    if f.get(flags.LETTER_TO_HANNE):
        did.append("you gave Hanne her mother's letter, five months late")
    if f.get(flags.TOLD_HANNE_TONIGHT):
        did.append("you told Hanne what the crosses were")
    if f.get(flags.OSKAR_GAVE_COLUMN) is True:
        did.append("you asked Oskar for the column instead of the stove")
    elif f.get(flags.OSKAR_GAVE_COLUMN) is False:
        did.append("you told Oskar to burn the column")
    if f.get(flags.COLUMN_TO_HANNE):
        did.append("you gave the column to Hanne")
    if f.get(flags.JORY_PLAYS) is True and f.get(flags.GUS_OPENS_THE_LORRY) is True:
        did.append("you got Maren's piano unstrapped for Jory, on your own head")
    elif f.get(flags.JORY_PLAYS) is True:
        did.append("you asked Jory to play her piano")
    elif f.get(flags.JORY_PLAYS) is False:
        did.append("you told Jory to save it for Monday")
    if f.get(flags.PER_TELLS_HER) is True:
        did.append("you told Per to tell her he had always known")
    elif f.get(flags.PER_TELLS_HER) is False:
        did.append("you told Per to let her go thinking nobody knew")
    if f.get(flags.INGRID_GIVES_BOOKS) is True:
        did.append("you talked the captain out of the side")
    elif f.get(flags.INGRID_GIVES_BOOKS) is False:
        did.append("you told the captain to do what she came to do")
    if f.get(flags.HANNE_KNOCKS) is True:
        did.append("you sent Hanne down to knock on six")
    elif f.get(flags.HANNE_KNOCKS) is False:
        did.append("you told Hanne to leave her be")
    if f.get(flags.AT_THE_STERN):
        if f.get(flags.BOOKS_TO_HANNE):
            did.append("at the stern, at five, you got the books into Hanne's hands")
        elif f.get(flags.BOOKS_KEPT):
            did.append("at the stern, at five, you told her to take them with her")
        elif f.get(flags.INGRID_GIVES_BOOKS) is not False:
            did.append("at the stern, at five, you watched them go")
    if not did:
        return (
            "WHAT YOU DID. Nothing that changed it. You poured coffee on the last "
            "night boat, and at five you were sent for."
        )
    joined = did[0] if len(did) == 1 else "; ".join(did[:-1]) + "; and " + did[-1]
    return "WHAT YOU DID. " + joined[0].upper() + joined[1:] + "."


def _hanneWithoutTheBooks(state, extra):
    if carried.hanneKnows(state):
        how = (
            " She knows where her mother went, and who with."
            if carried.hanneKnewInOctober(state)
            else " She knows now where her mother went, and who with, because "
            "you told her on the last night boat."
        )
        return (
            "HANNE." + how + " She will never know which of those Fridays were "
            "happy, because the only record of it went into the water "
            "mid-channel, or south in a suitcase." + extra
        )
    return (
        "HANNE. She still doesn't know what the crosses were. Two hundred and "
        "twenty-six of them, and nobody on the last night boat told her, though "
        "the answer crossed with her in cabin 6." + extra
    )


def _ingridModifiers(state):
    extra = ""
    if state.flags.get(flags.PER_TELLS_HER) is True:
        extra += (
            " At midnight Per told her he had always known, and was glad. She "
            "has written to him from Tromsund, the first letter she has written "
            "to anyone in thirty years."
        )
    if state.flags.get(flags.OPENED_SIX_AGAIN):
        extra += " She noticed the string had been retied. She has not said so."
    if state.pastFlag(flags.KEPT_INGRIDS_SECRET) is True and (
        state.flags.get(flags.TOLD_HANNE_TONIGHT)
        or state.flags.get(flags.LETTER_TO_HANNE)
    ):
        extra += (
            " You promised her in October that you would keep it, and in March "
            "you told Hanne. She says five months was long enough to keep "
            "anything, and does not quite mean it."
        )
    return extra


def _everyoneElse(state):
    f = state.flags
    lines = []

    per = f.get(flags.PER_TELLS_HER)
    if per is True:
        perLine = (
            "PER. He told her at the change of watch, nineteen years late, that "
            "he had always known and was glad. It cost him the one thing he had "
            "never said, and he says it was cheap."
        )
    elif per is False:
        perLine = (
            "PER. He let her go thinking nobody knew, because you told him to, "
            "and because it was what she wanted. He will think of the words he "
            "did not say every time he passes a night boat."
        )
    else:
        perLine = (
            "PER. Nobody asked him anything. He brought the Kittiwake into Brekka "
            "for the last time, and wrote 'Master below' in the log at midnight "
            "one last time, in his own hand."
        )
    if f.get(flags.BOOKS_OVERBOARD):
        perLine += (
            " He stopped the engines for it, as the night book said, and logged "
            "it as 'two minutes, master's order', though she was not master."
        )
    lines.append(perLine)

    cleared = carried.oskarCleared(state)
    pension = (
        " He has his pension; Raske's report saw to that."
        if cleared
        else " He has his pension, since the inquiry could prove nothing."
    )
    column = f.get(flags.OSKAR_GAVE_COLUMN)
    if column is True and f.get(flags.COLUMN_TO_HANNE):
        lines.append(
            "OSKAR. He tore the column out of nineteen ledgers for you, and you "
            "gave it to Hanne, which was who he meant by 'somebody'. There is no "
            "purser on a day boat." + pension
        )
    elif column is True:
        lines.append(
            "OSKAR. He tore the column out for you, and it is still in your "
            "jacket. One day he will ask who it went to. There is no purser on a "
            "day boat." + pension
        )
    elif column is False:
        lines.append(
            "OSKAR. He burned the column in the galley stove at four, because you "
            "said it was theirs. Nineteen years of Fridays in his hand, gone in a "
            "minute. There is no purser on a day boat." + pension
        )
    else:
        lines.append(
            "OSKAR. He burned the column in the galley stove at four, as he "
            "meant to, and nobody asked him not to. There is no purser on a day "
            "boat." + pension
        )

    opened = f.get(flags.GUS_OPENS_THE_LORRY)
    if opened is True and f.get(flags.PIANO_PLAYED):
        lines.append(
            "GUS. He cut the straps because you answered for it, and sat on a "
            "fish box and listened with his flask going cold. The saleroom found "
            "a scratch on the lid and docked him nothing; he says it was there in "
            "September."
        )
    elif opened is True:
        lines.append(
            "GUS. He cut the straps because you answered for it, and nobody came "
            "down to play, and he strapped it all again at four. He delivered "
            "it to the saleroom for the third time and the last."
        )
    elif opened is False:
        lines.append(
            "GUS. He kept it strapped, because it was sold, and was sorry. He "
            "delivered Maren's piano to the Brekka saleroom for the third time "
            "and the last."
        )
    else:
        lines.append(
            "GUS. He delivered Maren's piano to the Brekka saleroom for the third "
            "time and the last, and went home on the day boat."
        )

    plays = f.get(flags.JORY_PLAYS)
    if f.get(flags.PIANO_PLAYED):
        joryLine = (
            "JORY. He played the Grieg on her piano on the car deck in the middle "
            "of the night, to a lorry driver and a steward, and did not freeze. "
            "On Monday at ten he plays it again for the conservatory."
        )
        if f.get(flags.INGRID_HEARD_THE_PIANO):
            joryLine += " The captain heard it in six. He doesn't know that."
    elif plays is True:
        joryLine = (
            "JORY. He would have played it. The lorry stayed strapped. On Monday "
            "he plays the Grieg to a panel, on a piano he has never touched."
        )
    elif plays is False:
        joryLine = (
            "JORY. He saved it for Monday, because you told him to. He will sit "
            "down at ten o'clock not having touched a piano since August."
        )
    else:
        joryLine = (
            "JORY. Nobody asked him about Monday. He went down the ramp in Brekka "
            "with the music in his coat and Maren's piano on a lorry behind him."
        )
    lines.append(joryLine)

    if f.get(flags.OPENED_SIX_AGAIN):
        lines.append(
            "YOU. You opened six while she was on the bridge - her one rule "
            "tonight%s. Oskar saw the string had been retied. There is no Friday "
            "boat left to be kept on for, so it cost you only his good opinion, "
            "and you find you minded."
            % (", as you broke his in October" if carried.firedInOctober(state) else "")
        )
    elif carried.firedInOctober(state):
        lines.append(
            "YOU. Oskar did not keep you on after October, and asked you back for "
            "the last night anyway. You kept her rule. There is no more night "
            "boat to be kept on for."
        )
    else:
        lines.append(
            "YOU. You kept her rule, as you kept his in October. There is no more "
            "night boat. Oskar has written you a reference that says you can be "
            "trusted with a master key, which is the best thing he knows how to "
            "say about anyone."
        )
    return lines


def _fromOctober(state):
    """The people from the first crossing who are not aboard the last."""
    fenn = state.pastFlag(flags.FENN_TELLS)
    if fenn is True:
        fennLine = (
            "Dr Fenn went to live with his son in Brekka in February; Hanne has "
            "kept the card he sent her at Christmas."
        )
    else:
        fennLine = (
            "Dr Fenn went to live with his son in Brekka in February, with the "
            "crossword still not finished."
        )
    if state.pastFlag(flags.LETTER_DELIVERED):
        toveLine = (
            "Tove Ness took the job at the Halde care home, and was on the quay to "
            "see the last night boat go."
        )
    elif carried.letterInYourPocket(state) and state.flags.get(flags.LETTER_TO_HANNE):
        toveLine = (
            "Tove Ness took the job at the Halde care home. The letter she gave "
            "you in October reached Hanne in March, which is not what she was "
            "promised, and is perhaps better."
        )
    elif carried.letterInYourPocket(state):
        toveLine = (
            "Tove Ness took the job at the Halde care home and believes, still, "
            "that the letter she gave you in October was delivered."
        )
    else:
        toveLine = (
            "Tove Ness took the job at the Halde care home; she walked Maren's "
            "letter up to Harbour House a week after the funeral, and never "
            "learned what came of it."
        )
    raske = state.pastFlag(flags.TOLD_RASKE)
    if raske is True:
        raskeLine = (
            "Raske's report put the captain's name before the board; he left the "
            "company in January, and nobody on Halde knows why."
        )
    else:
        raskeLine = (
            "Raske signed the Kittiwake over to her buyer and went back to his "
            "office; his report still says what the columns said."
        )
    return "FROM OCTOBER. " + " ".join([fennLine, toveLine, raskeLine])


# --- the four endings ---------------------------------------------------------
def _onWhichDays(state):
    if state.flags.get(flags.HANNE_KNOCKS) is True:
        opening = (
            "WHAT HAPPENED. Nothing went over the side. In the small hours Hanne "
            "Sollid went down to cabin 6 and knocked, and the door opened, and "
            "Ingrid Halvard gave her nineteen years of crossword books and read "
            "her the margins: which days. At five Per stopped the engines as the "
            "night book said, and the two minutes went by with nothing to do in "
            "them. At six the last night boat came into Brekka, and the two of "
            "them went down the ramp together, Hanne carrying the box."
        )
    else:
        opening = (
            "WHAT HAPPENED. Nothing went over the side. At five o'clock the "
            "Kittiwake stopped her engines mid-channel for two minutes, and at the "
            "stern rail Ingrid Halvard gave Hanne Sollid nineteen years of "
            "crossword books and read her the margins: which days. At six the last "
            "night boat came into Brekka, and the two of them went down the ramp "
            "together, Hanne carrying the box."
        )
    column = (
        " Oskar's column is folded inside the last diary: the dates in a purser's "
        "hand, which match."
        if state.flags.get(flags.COLUMN_TO_HANNE)
        else ""
    )
    hanne = (
        "HANNE. She has the days. Two hundred and twenty-six crosses in her "
        "mother's diaries, and beside most of them now, in her mother's round "
        "print, 'Happy. - M.' It cost her the last of what she thought she knew "
        "about her parents' marriage, and she says she would pay it twice." + column
    )
    ingrid = (
        "INGRID. She gave the only record away, into the right hands, and took "
        "the Tuesday train south anyway - with an address in her pocket that is "
        "Hanne's, and a promise to come back for the stone in May. It cost her "
        "the thing she meant to do at five, and she is relieved."
        + _ingridModifiers(state)
    )
    close = (
        "WHAT IT WAS. A woman asked, in a letter, for her daughter to be told that "
        "she was happy, and on which days. On the last night boat, five months "
        "late, somebody did."
    )
    return opening, hanne, ingrid, close


def _overTheSide(state):
    opening = (
        "WHAT HAPPENED. At five o'clock the Kittiwake stopped her engines "
        "mid-channel for two minutes, and Ingrid Halvard put nineteen years of "
        "crossword books over the stern, one at a time, and the wake took them. "
        "At six the last night boat came into Brekka. Hanne Sollid went down the "
        "ramp with her mother's diaries - two hundred and twenty-six crosses, and "
        "not a word beside any of them."
    )
    hanne = _hanneWithoutTheBooks(state, "")
    ingrid = (
        "INGRID. She did what she came to do, and took the train south on Tuesday "
        "with a suitcase and nothing else. It cost her nothing she can name, and "
        "she will be naming it for the rest of her life." + _ingridModifiers(state)
    )
    close = (
        "WHAT IT WAS. Nineteen years kept from the record, and kept. Maren asked "
        "for her daughter to be told which days; the days are mid-channel between "
        "Halde and Brekka, and only the captain remembers them."
    )
    return opening, hanne, ingrid, close


def _theColumn(state):
    opening = (
        "WHAT HAPPENED. At five o'clock the Kittiwake stopped her engines "
        "mid-channel for two minutes, and Ingrid Halvard put nineteen years of "
        "crossword books over the stern, one at a time. At six the last night "
        "boat came into Brekka, and Hanne Sollid went down the ramp with Oskar's "
        "column folded into her mother's last diary: cabin 6, M. Sollid, every "
        "Friday, cash, paid in full."
    )
    hanne = (
        "HANNE. She has the dates, in the purser's hand, and the crosses, in her "
        "mother's, and every one matches. She does not have what was said on any "
        "of them; that went over the side at five. It is less than the books and "
        "more than nothing, and a man who kept it for nineteen years gave it to "
        "her by way of you."
    )
    ingrid = (
        "INGRID. She did what she came to do, and took the train south on Tuesday "
        "not knowing that the dates had gone ashore in Hanne's coat. Oskar will "
        "tell her, one day, by letter." + _ingridModifiers(state)
    )
    close = (
        "WHAT IT WAS. The words went into the water and the dates came ashore. "
        "Maren asked for her daughter to be told which days, and she was - in a "
        "purser's column, which is how the island has always kept its secrets."
    )
    return opening, hanne, ingrid, close


def _keptFromTheRecord(state):
    opening = (
        "WHAT HAPPENED. At five o'clock the engines stopped for two minutes, and "
        "nothing went over the side: you told her to take them with her, and she "
        "did. At six the last night boat came into Brekka, and Ingrid Halvard "
        "went down the ramp with a suitcase and a cardboard box marked BALLAST, "
        "and on Tuesday she took them south."
    )
    hanne = _hanneWithoutTheBooks(
        state,
        " The books are in a spare room in Tromsund, under a bed, and nobody will "
        "open the box until there is a house clearance.",
    )
    ingrid = (
        "INGRID. She kept them. It cost her nothing tonight; it will cost whoever "
        "opens the box, one day, and it will not be Hanne." + _ingridModifiers(state)
    )
    close = (
        "WHAT IT WAS. You told a woman she could keep what was hers, and she did. "
        "Nineteen years of which days, in a box, in the south. Whether that was a "
        "kindness is the question you take ashore, again."
    )
    return opening, hanne, ingrid, close
