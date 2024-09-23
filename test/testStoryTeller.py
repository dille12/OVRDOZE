from utilities.storyTeller import storyTeller
if __name__ == "__main__":
    st = storyTeller(None, None)
    for i in range(100):
        st.ammoUpdate("9MM")
    for i in range(200):
        st.ammoUpdate("7.62x39MM")
    for i in range(150):
        st.ammoUpdate("Energy Cell")
    print(st.ammoShot)