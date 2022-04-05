try:
    import engine
    import gui

except Exception as e:
    print("An error occurred in the Sandsea callback:")
    print(str(e))
    input("[ENTER] to exit")
