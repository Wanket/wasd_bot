from string import Template


class AnswerSubstitutionTemplate(Template):
    idpattern = r"(?!)"
    braceidpattern = r'(?a:[_a-z][a-z0-9_]*(?:\([^)]*\))?)'
