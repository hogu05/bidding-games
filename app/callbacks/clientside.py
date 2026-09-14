from dash import Input, Output

import ids
from dash_app import app

_REFIT_GRAPH_JS = """
function(_style) {
    function findCy(node) {
        if (!node) {
            return null;
        }
        if (node._cyreg && node._cyreg.cy) {
            return node._cyreg.cy;
        }
        var children = node.children || [];
        for (var i = 0; i < children.length; i++) {
            var found = findCy(children[i]);
            if (found) {
                return found;
            }
        }
        return null;
    }

    var root = document.getElementById('graph');
    var cy = findCy(root);
    if (cy) {
        cy.resize();
        cy.layout({name: 'breadthfirst', directed: true}).run();
    }
    return window.dash_clientside.no_update;
}
"""

app.clientside_callback(
    _REFIT_GRAPH_JS,
    Output(ids.GRAPH_REFRESH_DUMMY, "data"),
    Input(ids.GRAPH, "style"),
    prevent_initial_call=True,
)

_MIRROR_GRAPH_JS = """
function(_elements) {
    function findCy(node) {
        if (!node) {
            return null;
        }
        if (node._cyreg && node._cyreg.cy) {
            return node._cyreg.cy;
        }
        var children = node.children || [];
        for (var i = 0; i < children.length; i++) {
            var found = findCy(children[i]);
            if (found) {
                return found;
            }
        }
        return null;
    }

    var root = document.getElementById('graph');
    var cy = findCy(root);
    if (cy) {
        if (!cy._mirrorAttached) {
            cy._mirrorAttached = true;
            cy.on('layoutstop', function() {
                var bbox = cy.elements().boundingBox();
                cy.nodes().positions(function(node) {
                    var p = node.position();
                    return {x: bbox.x1 + bbox.x2 - p.x, y: p.y};
                });
            });
        }
        cy.layout({name: 'breadthfirst', directed: true}).run();
    }
    return window.dash_clientside.no_update;
}
"""

app.clientside_callback(
    _MIRROR_GRAPH_JS,
    Output(ids.GRAPH_MIRROR_DUMMY, "data"),
    Input(ids.GRAPH, "elements"),
)
