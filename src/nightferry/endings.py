# @author Daniel McCoy Stephenson
"""The last page: what the night came to, said plainly.

An ending is the one place the game is allowed to stop being coy. Each one
says what happened, who cabin 6 was for, what the player did, and what it
cost whom - every person on the boat, by name, in a sentence of their own -
in that order. The sentences are the choices people remembered, so a
player can see the line from a thing they said at nine o'clock to the way
the morning went.
"""

from nightferry import facts, flags

OFF_THE_LIGHT = "off_the_light"
BESIDE_ARNE = "beside_arne"
AT_THE_DOOR = "at_the_door"
KEPT_CROSSING = "kept_crossing"

ENDINGS = (OFF_THE_LIGHT, BESIDE_ARNE, AT_THE_DOOR, KEPT_CROSSING)

NAMES = {
    OFF_THE_LIGHT: "off the light",
    BESIDE_ARNE: "beside Arne",
    AT_THE_DOOR: "at the door",
    KEPT_CROSSING: "the kept crossing",
}


def name(state):
    """What the ending is called, for the save menu and the header."""
    return NAMES.get(state.ending, "docked")


def atTheQuay(state):
    """Which ending six o'clock comes to, if five o'clock did not end it."""
    if state.flags.get(flags.AT_THE_DOOR):
        return AT_THE_DOOR
    if state.flags.get(flags.HANNE_KNOWS):
        return BESIDE_ARNE
    return KEPT_CROSSING


def text(state):
    """The ending page for the ending the state has come to."""
    builders = {
        OFF_THE_LIGHT: _offTheLight,
        BESIDE_ARNE: _besideArne,
        AT_THE_DOOR: _atTheDoor,
        KEPT_CROSSING: _keptCrossing,
    }
    opening, hanne, ingrid, close = builders.get(state.ending, _keptCrossing)(state)
    return "\n\n".join(
        [opening, _whoItWasFor(state), _whatYouDid(state), "WHAT IT COST."]
        + [hanne, ingrid]
        + _everyoneElse(state)
        + [close]
    )


# --- shared paragraphs --------------------------------------------------------
def _whoItWasFor(state):
    said = (
        " Her letter to Ingrid, carried from the hospice by the nurse who sat "
        "with her, said: tell her I was happy, and on which days; then the "
        "light; not beside Arne - it was never him I crossed for."
        if state.flags.get(flags.LETTER_DELIVERED)
        else " She left a letter for Ingrid with the nurse who sat with her at the "
        "end. It was never delivered on the boat."
    )
    return (
        "WHO CABIN 6 WAS FOR. Maren Sollid, the Halde schoolteacher, who died "
        "in August. For nineteen years, from the spring after her husband "
        "died, she came home from Brekka on the Friday boat once a month, in "
        "cabin 6, and when the mate took the watch at midnight the captain, "
        "Ingrid Halvard, went down to her. The specialist was the crossing; Dr "
        "Fenn wrote the referrals and never asked. Three weeks ago Ingrid paid "
        "cash for the cabin in Maren's name so that she could come home in it "
        "once more. She came home in a canvas bag at her daughter's feet "
        "instead." + said
    )


def _whatYouDid(state):
    did = []
    if state.flags.get(flags.INGRID_TOLD_YOU) and not state.flags.get(
        flags.AT_THE_DOOR
    ):
        did.append("you found out who cabin 6 was for and heard it from the captain")
    elif state.knows(facts.THE_CAPTAIN) and not state.flags.get(flags.AT_THE_DOOR):
        did.append("you found out who cabin 6 was for")
    if state.flags.get(flags.TOVE_GAVE_LETTER) is True and state.flags.get(
        flags.LETTER_DELIVERED
    ):
        did.append("you carried Maren's letter to the bridge")
    elif state.flags.get(flags.TOVE_GAVE_LETTER) is False:
        did.append("you took the nurse up to the bridge with Maren's letter")
    if state.flags.get(flags.KEPT_INGRIDS_SECRET) is True:
        did.append("you promised the captain you would keep it")
    if state.flags.get(flags.ASHES_IN_SIX):
        did.append(
            "you carried Hanne's bag to cabin 6 for an hour while she slept, and "
            "brought it back before she woke"
        )
    if state.flags.get(flags.TOLD_HANNE):
        did.append("you told Hanne yourself")
    if state.flags.get(flags.MET_IN_WHEELHOUSE):
        did.append("you brought Hanne up to the bridge to hear it from Ingrid")
    if state.flags.get(flags.HANNE_CHOSE_LIGHT) is True:
        did.append("you told Hanne to do what her mother asked")
    elif state.flags.get(flags.HANNE_CHOSE_LIGHT) is False:
        did.append("you told Hanne the choice was hers, not her mother's")
    if state.flags.get(flags.INGRID_WILL_STOP) and not state.flags.get(
        flags.MET_IN_WHEELHOUSE
    ):
        did.append("you asked the captain to stop her ship")
    if state.flags.get(flags.AT_THE_DOOR):
        did.append(
            "when it came out, at four, it came out without you: you were "
            "fetched to the corridor like everyone else"
        )
    if not did:
        return "WHAT YOU DID. Nothing that changed it. You poured coffee."
    if len(did) == 1:
        joined = did[0]
    else:
        joined = "; ".join(did[:-1]) + "; and " + did[-1]
    return "WHAT YOU DID. " + joined[0].upper() + joined[1:] + "."


def _ingridModifiers(state):
    extra = ""
    if state.flags.get(flags.BROKE_YOUR_WORD):
        extra += (
            " You promised her you would keep it, and then you told Hanne. She "
            "knows. She has not decided whether to forgive you, and suspects "
            "she already has."
        )
    if state.flags.get(flags.INGRID_SAW_THE_SEAL):
        extra += (
            " And she knows you opened Maren's letter before you gave it to her. "
            "She has not said so to anyone, and will not."
        )
    return extra


def _everyoneElse(state):
    lines = []
    # Oskar and Raske: the one column in the books.
    told = state.flags.get(flags.TOLD_RASKE)
    if told is True:
        lines.append(
            "OSKAR. Cleared. Raske's report says every krone was in the till "
            "and none of it was ever the purser's. The price of that was the "
            "captain's name in the board's papers, and Oskar knows who paid it."
        )
        lines.append(
            "RASKE. You told him the truth, and he cleared Oskar with it. To do "
            "that he had to write that the bookings were the master's private "
            "arrangement. With the sale coming, the board will want her ashore "
            "before March. He did not enjoy writing it."
        )
    else:
        why = (
            "because you told Raske you knew nothing"
            if told is False
            else "because nobody told Raske what the bookings were"
        )
        lines.append(
            "OSKAR. Raske's report went in as the columns read - irregular cash "
            "bookings, purser responsible - %s. Oskar is suspended pending an "
            "inquiry. He will not explain the column; he would sooner lose the "
            "pension." % why
        )
        lines.append(
            "RASKE. %s His report says what the columns say, and Ingrid's name "
            "is nowhere in it."
            % (
                "You told him you knew nothing, and he did not believe you."
                if told is False
                else "He never found out who M. Sollid was."
            )
        )
    if state.ending == OFF_THE_LIGHT:
        lines[-1] += (
            " He was on deck when the engines stopped at the light, with his "
            "hat off. The report does not mention it."
        )

    fenn = state.flags.get(flags.FENN_TELLS)
    if fenn is True:
        lines.append(
            "DR FENN. He told Hanne he wrote nineteen years of false referrals "
            "for her mother and would write them again, because you asked him "
            "to. It cost him her good opinion for about a minute. She knew "
            "something good before she knew what."
        )
    elif fenn is False:
        lines.append(
            "DR FENN. He let it lie, because you told him to. The referrals go "
            "into the ground with Maren, and nobody will ask him again."
        )
    else:
        lines.append(
            "DR FENN. Nobody asked him what he knew. He went ashore with the "
            "crossword finished but for seven down."
        )

    jory = state.flags.get(flags.JORY_TELLS)
    if jory is True:
        joryLine = (
            "JORY. He told his parents on the quay, before the banner was "
            "unrolled, that he has left the conservatory. His mother cried; his "
            "father said 'well, then'; they took him home anyway."
        )
    elif jory is False:
        joryLine = (
            "JORY. He is keeping it until after Saturday. He will stand at the "
            "funeral in the suit they bought him for recitals."
        )
    else:
        joryLine = (
            "JORY. He went down the ramp to a banner that said WELCOME HOME, and "
            "nobody on the boat had asked him anything."
        )
    if state.ending == OFF_THE_LIGHT:
        joryLine += (
            " He was at the rail when the engines stopped. Afterwards he asked "
            "the captain whether Harbour House would want someone to play the "
            "piano."
        )
    lines.append(joryLine)

    gus = state.flags.get(flags.LET_GUS_IN)
    if gus is True:
        lines.append(
            "GUS. He slept in cabin 6 because you let him%s. His back is better. "
            "He delivered the piano to Harbour House at seven and found out "
            "whose it had been, and has not stopped apologising."
            % (
                ", and the captain found him there at four"
                if state.flags.get(flags.AT_THE_DOOR)
                else ""
            )
        )
    elif gus is False:
        lines.append(
            "GUS. He slept in his cab, because you said the cabin was spoken "
            "for. His back remembers you. He delivered the piano to Harbour "
            "House at seven."
        )
    else:
        lines.append(
            "GUS. He delivered the piano to Harbour House at seven and never "
            "knew whose it had been."
        )

    tove = state.flags.get(flags.TOVE_GAVE_LETTER)
    if tove is True and not state.flags.get(flags.LETTER_DELIVERED):
        lines.append(
            "TOVE. She trusted you with the thing Maren said mattered most, and "
            "you never took it up the stairs. It is still in your inside pocket. "
            "She thinks it was delivered."
        )
    elif tove is True:
        lines.append(
            "TOVE. She trusted a steward she had known for ten minutes with the "
            "thing Maren said mattered most, and it got there.%s She is going to "
            "look at the job at the care home."
            % (" You read it first. She will never know." if state.flags.get(flags.READ_THE_LETTER) else "")
        )
    elif tove is False:
        lines.append(
            "TOVE. She climbed to the bridge herself and asked 'Are you I.H.?', "
            "and was told yes. She is going to take the job at the care home, "
            "she thinks."
        )
    elif state.flags.get(flags.LETTER_DELIVERED):
        lines.append(
            "TOVE. She heard her own patient's name through the door of cabin 4 "
            "at four in the morning and gave the letter over in a corridor. It "
            "got there. Not the way she had pictured."
        )
    else:
        lines.append(
            "TOVE. She went ashore with the letter still sealed in her holdall. "
            "On Halde someone will tell her whose initials they are, and she "
            "will walk up to Harbour House with it a week after the funeral. "
            "The first line says 'If H. is on the boat, tell her.' What Ingrid "
            "does with that, a week late, is up to Ingrid."
        )

    if state.flags.get(flags.OPENED_SIX):
        lines.append(
            "YOU. You opened cabin 6%s - the one thing Oskar asked you not to "
            "do. He will not keep you on. You knew the rule and you knew why "
            "it might matter, and you opened it anyway."
            % (" for a lorry driver" if state.flags.get(flags.LET_GUS_IN) else "")
        )
    else:
        lines.append(
            "YOU. You never opened cabin 6. Oskar has asked whether you will do "
            "the Friday boat again, for as long as there is one."
        )
    return lines


# --- the four endings ---------------------------------------------------------
def _offTheLight(state):
    how = "on the bridge, because you brought her up"
    if state.flags.get(flags.AT_THE_DOOR):
        how = "in a corridor at four in the morning"
    elif state.flags.get(flags.TOLD_HANNE):
        how = "from you, in the saloon"
    opening = (
        "WHAT HAPPENED. At five o'clock the Kittiwake stopped her engines off "
        "the Halde light, for the first time in twenty-two years of Friday "
        "nights, and Hanne Sollid and Ingrid Halvard put Maren into the water "
        "from the stern, together, as she had asked. Then the ship went on, "
        "and docked at six, and the island was waiting for a funeral."
    )
    hanne = (
        "HANNE. She found out %s, and she did what her mother asked, knowing "
        "why. It cost her the churchyard: tomorrow the island comes to a "
        "funeral at a grave with her mother's name already cut on the stone, "
        "and Hanne will have to stand there and say it is empty, and decide "
        "how much of why to say." % how
    )
    ingrid = (
        "INGRID. She stopped her ship at the light with the company's man "
        "aboard, and stood at the rail with Maren's daughter and said goodbye "
        "where she could see it. It may cost her her last winter in command. "
        "She says the company can write her a letter." + _ingridModifiers(state)
    )
    close = (
        "WHAT IT WAS. A woman who crossed for nineteen years to be happy for "
        "ten hours at a time, and asked to be put into the water where the "
        "crossing ended. Her daughter and the woman she crossed for did it "
        "together, because somebody carried the right things up the right "
        "stairs in time."
    )
    return opening, hanne, ingrid, close


def _besideArne(state):
    opening = (
        "WHAT HAPPENED. The Kittiwake docked at six. Hanne Sollid went down "
        "the ramp with her mother in the canvas bag, knowing who cabin 6 had "
        "been for, and tomorrow Maren will be buried beside Arne under the "
        "stone that already has her name on it."
    )
    chose = state.flags.get(flags.HANNE_CHOSE_LIGHT)
    if chose is False:
        hanne = (
            "HANNE. She knows, and she chose the churchyard, after you told "
            "her the choice was hers and not her mother's. It cost her mother's "
            "last wish, knowingly. She has asked the captain to come, and to "
            "stand at the back."
        )
    elif chose is True:
        hanne = (
            "HANNE. She wanted the light, and said so, and nobody asked the "
            "captain to stop. She stood at the rail with the bag while the "
            "Halde light went by at twelve knots. It cost her mother's last "
            "wish, and she did not choose to lose it."
        )
    else:
        hanne = (
            "HANNE. She knows, and nobody asked her what she wanted to do with "
            "it before the light went by. On the quay she took the bag to the "
            "churchyard because the stone was cut."
        )
    ingrid = (
        "INGRID. Hanne knows; she did not hear it from Ingrid on the bridge. "
        "Ingrid will go to the funeral and stand at the back, beside a grave "
        "Maren asked not to be put in." + _ingridModifiers(state)
    )
    close = (
        "WHAT IT WAS. The truth reached the one person who had a right to it, "
        "in time to choose. Maren lies beside Arne, which she asked not to; her "
        "daughter knows why, and the light went by."
    )
    return opening, hanne, ingrid, close


def _atTheDoor(state):
    opening = (
        "WHAT HAPPENED. At four in the morning the captain came down to cabin "
        "6, because nobody else had, and Hanne Sollid was in the corridor with "
        "her mother in her arms. It came out there, between the fire hose and "
        "the linen cupboard. At six the Kittiwake docked, and Hanne went down "
        "the ramp to a funeral with her mother's name already on the stone."
    )
    hanne = (
        "HANNE. She found out in a corridor at four in the morning, from a "
        "woman she had never met, with the bag in her arms.%s She has her "
        "mother's own words now, read aloud by the person they were written "
        "to. On the quay she walked past Ingrid without speaking. What she does "
        "tomorrow, she has not said."
        % (
            " Dr Fenn had told her, earlier in the night, that her mother went "
            "somewhere every month that made her happy; it was the only thing "
            "that made the corridor bearable."
            if state.flags.get(flags.HANNE_PREPARED)
            else ""
        )
    )
    ingrid = (
        "INGRID. She said it at the door of cabin 6, which she had not been able "
        "to open for three weeks%s. It was not the way either of them would have "
        "chosen." % (
            ", and found a lorry driver asleep in it" if state.flags.get(flags.LET_GUS_IN) else ""
        )
        + _ingridModifiers(state)
    )
    close = (
        "WHAT IT WAS. Nobody chose how it came out. It came out anyway, because "
        "a captain could not leave an empty cabin empty any longer. Everyone "
        "knows now, and it was said in the worst place it could have been."
    )
    return opening, hanne, ingrid, close


def _keptCrossing(state):
    opening = (
        "WHAT HAPPENED. The Kittiwake docked at six. Hanne Sollid went down the "
        "ramp with her mother in the canvas bag, not knowing who cabin 6 had "
        "been for, and tomorrow she will bury her beside Arne under the stone "
        "that already has her name on it. The captain watched her go from the "
        "bridge wing."
    )
    hanne = (
        "HANNE. She went ashore not knowing. She will put her mother beside her "
        "father with the note still in her pocket - 'not beside Arne' - and "
        "think for the rest of her life that her mother was not thinking "
        "straight at the end. That is the cost, and it is all hers, and unless "
        "somebody tells her she will never know she paid it."
    )
    if state.flags.get(flags.ASHES_IN_SIX):
        hour = (
            " For an hour, while Hanne slept, Maren was in cabin 6, where she "
            "always crossed, and Ingrid sat with her. She had her last crossing."
        )
    else:
        hour = (
            " She stayed on the bridge all night, and Maren crossed on the saloon "
            "floor two decks below her."
        )
    ingrid = (
        "INGRID. You kept her secret, as you said you would." + hour + " She will "
        "go to the funeral and stand at the back, and nobody will know why."
        + _ingridModifiers(state)
    )
    close = (
        "WHAT IT WAS. You were trusted with something and you kept it. A "
        "daughter buried her mother not knowing she had been happy, or where. "
        "Whether that was a kindness is the question you take ashore."
    )
    return opening, hanne, ingrid, close
