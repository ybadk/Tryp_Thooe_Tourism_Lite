#!/usr/bin/env python3
"""
Test script to verify developer details have been updated correctly.
This script loads the developer_details.csv file and displays the information.
"""

import pandas as pd
import os


def test_developer_details():
    """Test that only Kgothatso Thooe's details are loaded"""

    # Check if the file exists
    csv_file = 'developer_details.csv'
    if not os.path.exists(csv_file):
        print(f"❌ Error: {csv_file} not found")
        return False

    try:
        # Load the developer details
        df = pd.read_csv(csv_file)

        print("📋 Developer Details Test Results:")
        print("=" * 50)

        # Check number of developers
        num_developers = len(df)
        print(f"Number of developers: {num_developers}")

        if num_developers == 1:
            print("✅ Correct: Only 1 developer found")
        else:
            print(f"❌ Error: Expected 1 developer, found {num_developers}")
            return False

        # Check if it's Kgothatso Thooe
        developer = df.iloc[0]
        name = developer['name']
        email = developer['email']
        role = developer['role']

        print(f"\n👤 Developer Information:")
        print(f"Name: {name}")
        print(f"Role: {role}")
        print(f"Email: {email}")

        if "Kgothatso Thooe" in name or "Thapelo" in name:
            print("✅ Correct: Developer is Kgothatso Thooe")
        else:
            print(f"❌ Error: Expected Kgothatso Thooe, found {name}")
            return False

        if "kgothatsothooe@gmail.com" in email:
            print("✅ Correct: Email is kgothatsothooe@gmail.com")
        else:
            print(f"❌ Error: Expected kgothatsothooe@gmail.com, found {email}")
            return False

        # Check GitHub username
        github = developer['github']
        if github == 'ybadk':
            print("✅ Correct: GitHub username is ybadk")
        else:
            print(f"❌ Error: Expected GitHub username ybadk, found {github}")
            return False

        # Check skills include Data Science
        skills = developer['skills']
        if "Data Science" in skills:
            print("✅ Correct: Skills include Data Science")
        else:
            print(f"❌ Error: Expected Data Science in skills, found: {skills}")
            return False

        print("\n🎉 All tests passed! Developer details have been updated correctly.")
        return True

    except Exception as e:
        print(f"❌ Error loading developer details: {e}")
        return False


if __name__ == "__main__":
    test_developer_details()
