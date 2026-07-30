#!/usr/bin/env python3
"""Extract all widget types and their specific properties from the SPJ file."""
import json, sys

with open(sys.argv[1], 'r') as f:
    data = json.load(f)

widgets = {}
all_strtypes = set()

def extract_widgets(obj, depth=0):
    if isinstance(obj, dict):
        objtype = obj.get('saved_objtypeKey', '')
        name = ''
        widget_props = []
        
        for prop in obj.get('properties', []):
            st = prop.get('strtype', '')
            all_strtypes.add(st)
            if st == 'OBJECT/Name':
                name = prop.get('strval', '')
            # Capture widget-specific properties (not OBJECT/ or _style/ or _event/)
            prefix = st.split('/')[0] if '/' in st else ''
            if prefix and prefix not in ('OBJECT', '_style', '_event', ''):
                sv = prop.get('strval', prop.get('intarray', prop.get('integer', '')))
                it = prop.get('InheritedType', '')
                part = prop.get('part', '')
                widget_props.append({
                    'strtype': st,
                    'InheritedType': it,
                    'value_example': str(sv)[:60],
                    'part': part
                })
        
        if objtype:
            if objtype not in widgets:
                widgets[objtype] = {'names': [], 'props': {}}
            widgets[objtype]['names'].append(name)
            for wp in widget_props:
                key = wp['strtype']
                if key not in widgets[objtype]['props']:
                    widgets[objtype]['props'][key] = wp
        
        for child in obj.get('children', []):
            extract_widgets(child, depth + 1)
    elif isinstance(obj, list):
        for item in obj:
            extract_widgets(item, depth)

# Handle both v1.5 and v1.6 format
root = data.get('root', data)
extract_widgets(root)

print("=" * 90)
print("WIDGET TYPES AND THEIR SPECIFIC PROPERTIES")
print("=" * 90)

for wtype in sorted(widgets.keys()):
    info = widgets[wtype]
    print(f"\n{'─' * 90}")
    print(f"  {wtype}  (instances: {', '.join(info['names'])})")
    print(f"{'─' * 90}")
    for st in sorted(info['props'].keys()):
        p = info['props'][st]
        part_info = f"  part={p['part']}" if p['part'] else ""
        print(f"    {st:<45} IT={p['InheritedType']:<3} val={p['value_example']}{part_info}")

print(f"\n\n{'=' * 90}")
print(f"ALL UNIQUE STRTYPES ({len(all_strtypes)} total)")
print(f"{'=' * 90}")
for st in sorted(all_strtypes):
    print(f"  {st}")
