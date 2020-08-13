class SymbolTable:
    def __init__(self):
        self.globalScope = dict()
        self.localScope = dict()
        self.globalScopeKindCount = {"STATIC": 0, "FIELD": 0, "ARG": 0, "VAR": 0}
        self.localScopeKindCount = {"STATIC": 0, "FIELD": 0, "ARG": 0, "VAR": 0}

    def startSubroutine(self):
        self.localScope = dict()
        self.localScopeKindCount = {"STATIC": 0, "FIELD": 0, "ARG": 0, "VAR": 0}

    def define(self, name, vartype, kind):
        if kind in ["STATIC", "FIELD"]:
            self.globalScope[name] = {"type": vartype, "kind": kind, "index": self.globalScopeKindCount[kind]}
            self.globalScopeKindCount[kind] += 1
        else:
            self.localScope[name] = {"type": vartype, "kind": kind, "index": self.localScopeKindCount[kind]}
            self.localScopeKindCount[kind] += 1

    def varCount(self, kind):
        if kind in ["STATIC", "FIELD"]:
            return self.globalScopeKindCount[kind]
        else:
            return self.localScopeKindCount[kind]

    def kindOf(self, name):
        if name in self.localScope.keys():
            return self.localScope[name]["kind"]
        elif name in self.globalScope.keys():
            return self.globalScope[name]["kind"]
        else:
            return "NONE"

    def typeOf(self, name):
        if name in self.localScope.keys():
            return self.localScope[name]["type"]
        elif name in self.globalScope.keys():
            return self.globalScope[name]["type"]
        else:
            return "NONE"

    def indexOf(self, name):
        if name in self.localScope.keys():
            return self.localScope[name]["index"]
        elif name in self.globalScope.keys():
            return self.globalScope[name]["index"]
        else:
            return "NONE"