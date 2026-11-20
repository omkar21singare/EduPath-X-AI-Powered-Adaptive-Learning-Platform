import re

files_to_fix = [
    "frontend/src/components/AdaptiveVisualizer.tsx",
    "frontend/src/components/BKTTrajectory.tsx",
    "frontend/src/components/KnowledgeMap.tsx",
    "frontend/src/components/ObservabilityPanel.tsx",
    "frontend/src/components/KPICards.tsx"
]

for file in files_to_fix:
    with open(file, 'r', encoding='utf-8') as f:
        content = f.read()
    content = content.replace("import React from 'react';\n", "")
    with open(file, 'w', encoding='utf-8') as f:
        f.write(content)

# BKTTrajectory: let chartData: any[] = [];
with open("frontend/src/components/BKTTrajectory.tsx", "r", encoding='utf-8') as f:
    content = f.read()
content = content.replace("let chartData = [];", "let chartData: any[] = [];")
with open("frontend/src/components/BKTTrajectory.tsx", "w", encoding='utf-8') as f:
    f.write(content)

# ObservabilityPanel: remove recentActivity
with open("frontend/src/components/ObservabilityPanel.tsx", "r", encoding='utf-8') as f:
    content = f.read()
content = content.replace("({ dashboardData, recentActivity }: any)", "({ dashboardData }: any)")
with open("frontend/src/components/ObservabilityPanel.tsx", "w", encoding='utf-8') as f:
    f.write(content)

print("Fixed TypeScript errors")
