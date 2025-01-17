import sys
import argparse
if __name__ == "__main__":
    from emulator import Emulator
    from assembler import Assembler
else:
    from .emulator import Emulator
    from .assembler import Assembler

"""
An example showing how to highlight a node or edge on selection
"""
import dash_interactive_graphviz
import dash
from dash.dependencies import Input, Output, State
import dash_html_components as html
import dash_core_components as dcc

app = dash.Dash(__name__)

# A simple list of edges
edges = [
    ("a", "b"),
    ("a", "c"),
    ("c", "b"),
    ("b", "a"),
]

app.layout = html.Div(
    [
        html.Div(
            dash_interactive_graphviz.DashInteractiveGraphviz(id="gv", dot_source="edges"),
            style=dict(flexGrow=1, position="relative"),
        )        
    ],
    style=dict(position="absolute", height="100%", width="100%", display="flex"),
)

@app.callback(
    Output("gv", "dot_source"),
    Input("gv", "selected_node"),
    Input("gv", "selected_edge"),
)
def show_graph(selected_node, selected_edge):
    """
    Based on the selected element this generates the correct dot file
    for component update.
    """
    # dictionary of all the nodes and if they are selected
    nodes = {node: node == selected_node for edge in edges for node in edge}

    lines = [
        "digraph {",
        "node [style=filled];"        
    ]
    for node, selected in nodes.items():
        color= 'green' if selected else 'grey'
        lines.append(f'{node}[color={color}];')

    for f,t in edges:
        line = f"{f}->{t}"
        color= '[color=red]' if (line == selected_edge) else ''
        line += color
        lines.append(line)

    lines.append("}")
    
#    dot = "\n".join(lines)
    print("tick")
    dot = emulator.start()
    return dot

parser = argparse.ArgumentParser(prog='pythonRSC', description="An emulator for the RSC architecture written in Python.")
parser.add_argument('mode', choices=["debug", "run", "assemble"])
parser.add_argument('filein', help="your microcode file which contains instructions")
parser.add_argument('-o', required="assemble" in sys.argv, help="the output file path for the assembler generated bytecode", type=str)
parser.add_argument('-cfg', action='store_true', help="indicates if you wish to see the control flow graph")
args = parser.parse_args(sys.argv[1:])
asm_obj = Assembler(args.filein)
debug_val = True if args.mode == "debug" else False
emulator = Emulator(asm_obj, debug_val, args.cfg)


def main():
    app.run_server(debug=True)

if __name__ == "__main__":
    main()
