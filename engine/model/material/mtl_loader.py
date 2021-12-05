from engine.model.material.material import Material


class MTLLoader:

    def __init__(self, content: list):
        self._content = [line.split() for line in content if len(line) > 1]
        self._materials = self._parse_materials()

    @staticmethod
    def load(relative_path: str):
        relative_path = relative_path.split('.')[0] + ".mtl"
        return MTLLoader(open(relative_path, 'r', encoding="utf-8").readlines(),)

    def _parse_materials(self) -> dict:
        result, content = {}, self._content
        i, j = 0, 0
        while i < len(content):
            if content[i][0] == 'newmtl' and content[i][1] not in result:
                result[content[i][1]] = {}
                j = i + 1
                while j < len(content) and content[j][0] != 'newmtl':
                    result[content[i][1]][content[j][0]] = self._get_value_from(content[j])
                    j += 1
            i += 1
        return {name: Material(metadata) for name, metadata in result.items()}

    def _get_value_from(self, value: str):
        if len(value) > 2:
            return [eval(item) for item in value[1:]]
        return eval(value[1])

    def get_materials(self):
        return self._materials
