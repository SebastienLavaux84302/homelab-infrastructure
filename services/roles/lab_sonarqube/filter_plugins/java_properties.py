"""Échappement des valeurs du fichier de configuration Java properties."""

from ansible.errors import AnsibleFilterError


def java_property(value):
    if not isinstance(value, str):
        raise AnsibleFilterError("Une valeur de propriété Java doit être une chaîne.")
    if "\x00" in value:
        raise AnsibleFilterError("Une valeur de propriété Java ne peut contenir NUL.")
    result = []
    escapes = {"\\": "\\\\", "\n": "\\n", "\r": "\\r", "\t": "\\t", "\f": "\\f"}
    for char in value:
        if char in escapes:
            result.append(escapes[char])
        elif char in " =:#!":
            result.append("\\" + char)
        elif ord(char) < 32 or ord(char) > 126:
            encoded = char.encode("utf-16-be", errors="surrogatepass")
            result.extend("\\u" + encoded[i:i + 2].hex() for i in range(0, len(encoded), 2))
        else:
            result.append(char)
    return "".join(result)


class FilterModule:
    def filters(self):
        return {"lab_java_property": java_property}
