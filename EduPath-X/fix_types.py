import os
import re

app_path = "frontend/src/App.tsx"
with open(app_path, "r", encoding="utf-8") as f:
    content = f.read()

# Replace const renderMainContent = () => { with const renderMainContent = (data: DashboardResponse) => {
content = content.replace("const renderMainContent = () => {", "const renderMainContent = (data: DashboardResponse) => {")

# Find the block inside renderMainContent and replace dashboardData with data
start_idx = content.find("const renderMainContent = (data: DashboardResponse) => {")
end_idx = content.find("};", start_idx) + 2
block = content[start_idx:end_idx]
block = block.replace("dashboardData.", "data.").replace("dashboardData?", "data?")
content = content[:start_idx] + block + content[end_idx:]

# Call renderMainContent(dashboardData)
content = content.replace("renderMainContent()", "renderMainContent(dashboardData)")

with open(app_path, "w", encoding="utf-8") as f:
    f.write(content)

# Fix other components
components_dir = "frontend/src/components"
for file in os.listdir(components_dir):
    if file.endswith(".tsx") and file in ["AIAssistantPage.tsx", "MyLearning.tsx", "PerformancePage.tsx", "PracticePage.tsx", "ProgressReportsPage.tsx", "SettingsPage.tsx"]:
        filepath = os.path.join(components_dir, file)
        with open(filepath, "r", encoding="utf-8") as f:
            c = f.read()
        c = c.replace("import React from 'react';\n", "")
        c = c.replace("import React, { useState } from 'react';\n", "")
        c = c.replace("import { QuizModal } from './QuizModal';\n", "")
        # Remove unused vars from PracticePage
        c = c.replace("{ dashboardData, onSelectConcept, onStartRecommendation }: any", "{ dashboardData, onStartRecommendation }: any")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(c)

print("Fixed types")
