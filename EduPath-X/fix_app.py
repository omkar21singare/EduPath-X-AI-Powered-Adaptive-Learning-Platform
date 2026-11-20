import os

app_path = "frontend/src/App.tsx"
with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "  const renderMainContent = () => {"
end_marker = "  };\n\n        <main className=\"p-8 space-y-6 flex-1\">"

if start_marker in content and end_marker in content:
    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker) + len("  };\n")
    render_func = content[start_idx:end_idx]
    
    # Remove it from current location
    content = content[:start_idx] + content[end_idx:]
    
    # Find eturn ( and insert it before
    return_idx = content.find("  return (\n")
    if return_idx != -1:
        content = content[:return_idx] + render_func + "\n" + content[return_idx:]
    
    with open(app_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("Fixed App.tsx")
else:
    print("Could not find markers")
