from pychord.constants.scales import SHARPED_SCALE, FLATTED_SCALE, SCALE_VAL_DICT

from constans import NOTES_IN_OCTAVE


def get_key_by_value(dictOfElements, valueToFind):
    for item in dictOfElements.items():
        if item[1] == valueToFind:
            return item[0]

    return None


def midi_to_note(number: int) -> tuple:
    # 'http://www.electronics.dit.ie/staff/tscarff/Music_technology/midi/midi_note_numbers_for_octaves.htm'

    octave = number // NOTES_IN_OCTAVE
    note = number % NOTES_IN_OCTAVE

    return note, octave


def notes_names_to_index(notes):
    conv_notes = []
    for item in notes:

        index = get_key_by_value(SHARPED_SCALE, item)
        if index is not None:
            conv_notes.append(index)
        else:
            index = get_key_by_value(FLATTED_SCALE, item)
            conv_notes.append(index)

    return conv_notes


def index_to_note_name(notes, scale):

    scale_notes = SCALE_VAL_DICT[scale]

    conv_notes = []
    for item in notes:
        conv_notes.append(scale_notes[item])

    return conv_notes


def midi_to_index(notes):
    conv_notes = []
    for item in notes:
        conv_notes.append(midi_to_note(item)[0])

    return conv_notes