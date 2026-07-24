import base64
import re
import urllib.parse
import urllib.request
import requests
from flask import Flask, jsonify, render_template, request

app = Flask(__name__)

# --- CURATED MASTER SONG CATALOG ---
MASTER_SONG_DATABASE = [
    {
        "title": "Saturn",
        "artist": "SZA",
        "id": "3OHfY25tqY28d16oZCLcet",
        "cover": "https://i.scdn.co/image/ab67616d0000b2737156f95085376781970bfd56",
        "platform": "spotify",
    },
    {
        "title": "Kill Bill",
        "artist": "SZA",
        "id": "1QrgL3Z3A0P3m3E5C3m3E5",
        "cover": "https://i.scdn.co/image/ab67616d0000b2737156f95085376781970bfd56",
        "platform": "spotify",
    },
    {
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "id": "0VjIjW4GlUZAMYd2vXMi3b",
        "cover": "https://i.scdn.co/image/ab67616d0000b2738863bc11d2aa12b54f5aeb36",
        "platform": "spotify",
    },
    {
        "title": "Save Your Tears",
        "artist": "The Weeknd",
        "id": "5QO79kh1waicV47BqGRL3g",
        "cover": "https://i.scdn.co/image/ab67616d0000b2738863bc11d2aa12b54f5aeb36",
        "platform": "spotify",
    },
    {
        "title": "Die For You",
        "artist": "The Weeknd",
        "id": "2LBqCSwoPIE93e6pPzL137",
        "cover": "https://i.scdn.co/image/ab67616d0000b2738863bc11d2aa12b54f5aeb36",
        "platform": "spotify",
    },
    {
        "title": "Excuses",
        "artist": "AP Dhillon, Gurinder Gill",
        "id": "2d1gRk45P7P1fBv95l7yE6",
        "cover": "https://i.scdn.co/image/ab67616d0000b2730248c8b6b0c268875505e94b",
        "platform": "spotify",
    },
    {
        "title": "Born to Shine",
        "artist": "Diljit Dosanjh",
        "id": "1m0oA9unQF33m3E5C3m3E5",
        "cover": "https://i.scdn.co/image/ab67616d0000b273b4823908f9fcf958b476f4e6",
        "platform": "spotify",
    },
    {
        "title": "Blue Eyes",
        "artist": "Yo Yo Honey Singh",
        "id": "5OJv1mF3j7sEaN6cR2t5fE",
        "cover": "https://i.scdn.co/image/ab67616d0000b273e120f269c28ae92fdacb3fd8",
        "platform": "spotify",
    },
    {
        "title": "Don't Let Me Down",
        "artist": "The Chainsmokers, Daya",
        "id": "4LDrohDJvVECNZIC81XDCa",
        "cover": "https://i.scdn.co/image/ab67616d0000b273d434af6c39a896d8ed50882e",
        "platform": "spotify",
    },
    {
        "title": "Lush Life",
        "artist": "Zara Larsson",
        "id": "35mvY5S1H3J2Qj5l3yE6",
        "cover": "https://i.scdn.co/image/ab67616d0000b273072295cccd4b80b7b1351df7",
        "platform": "spotify",
    },
    {
        "title": "Treat You Better",
        "artist": "Shawn Mendes",
        "id": "0B4g5R6tF9G9sN2tM8l0x6",
        "cover": "https://i.scdn.co/image/ab67616d0000b2736480b273934371fa9d1bb82e",
        "platform": "spotify",
    },
    {
        "title": "Control",
        "artist": "Armaan Malik",
        "id": "5PjdY0CKGZdEuoNab3yDmX",
        "cover": "https://i.scdn.co/image/ab67616d0000b273e38734994833aae40d5770d4",
        "platform": "spotify",
    },
    {
        "title": "Calm Down",
        "artist": "Selena Gomez, Rema",
        "id": "4LDrohDJvVECNZIC81XDCa",
        "cover": "https://i.scdn.co/image/ab67616d0000b273d434af6c39a896d8ed50882e",
        "platform": "spotify",
    },
    {
        "title": "Without Me",
        "artist": "Halsey",
        "id": "5CLGzJsGvhdxuCVn3tLq78",
        "cover": "https://i.scdn.co/image/ab67616d0000b273b49910dd84dae281514757c9",
        "platform": "spotify",
    },
    {
        "title": "Happier Than Ever",
        "artist": "Billie Eilish",
        "id": "4VxKeMohJjyIRrKmtkRtnU",
        "cover": "https://i.scdn.co/image/ab67616d0000b2732a392c640d2f0995fa6654b4",
        "platform": "spotify",
    },
    {
        "title": "Bad Guy",
        "artist": "Billie Eilish",
        "id": "2Fxmhks0bxGSBdJ92vM42m",
        "cover": "https://i.scdn.co/image/ab67616d0000b27350a300f07d645b6ef6d27300",
        "platform": "spotify",
    },
    {
        "title": "ocean eyes",
        "artist": "Billie Eilish",
        "id": "7hDVYcQq6MxkdJG678l9iM",
        "cover": "https://i.scdn.co/image/ab67616d0000b27350a300f07d645b6ef6d27300",
        "platform": "spotify",
    },
    {
        "title": "Closer",
        "artist": "The Chainsmokers, Halsey",
        "id": "7BKLCZ1jbUBVqRi2FVlTV4",
        "cover": "https://i.scdn.co/image/ab67616d0000b273a70faee80f08a9f029050d24",
        "platform": "spotify",
    },
]

SPOTIFY_RECOMMENDATIONS = {
    "happy": MASTER_SONG_DATABASE[5:10],
    "neutral": MASTER_SONG_DATABASE[2:5],
    "sad": MASTER_SONG_DATABASE[0:4],
    "angry": MASTER_SONG_DATABASE[15:17],
    "tired": MASTER_SONG_DATABASE[10:12],
    "fear": [MASTER_SONG_DATABASE[16]],
    "exhausted": [MASTER_SONG_DATABASE[4]],
}

ENGLISH_RECOMMENDATIONS = {
    "happy": [
        {
            "title": "Excuses",
            "artist": "AP Dhillon",
            "id": "iD9Z2g3F204",
            "cover": "https://img.youtube.com/vi/iD9Z2g3F204/hqdefault.jpg",
            "platform": "youtube",
        },
        {
            "title": "Don't Let Me Down",
            "artist": "The Chainsmokers",
            "id": "Io0fBr1XBUA",
            "cover": "https://img.youtube.com/vi/Io0fBr1XBUA/hqdefault.jpg",
            "platform": "youtube",
        },
        {
            "title": "Lush Life",
            "artist": "Zara Larsson",
            "id": "tglB9BUZZg0",
            "cover": "https://img.youtube.com/vi/tglB9BUZZg0/hqdefault.jpg",
            "platform": "youtube",
        },
        {
            "title": "Born to Shine",
            "artist": "Diljit Dosanjh",
            "id": "uV8qYw7zNko",
            "cover": "https://img.youtube.com/vi/uV8qYw7zNko/hqdefault.jpg",
            "platform": "youtube",
        },
    ],
    "neutral": [
        {
            "title": "Blinding Lights",
            "artist": "The Weeknd",
            "id": "4NRXx6U8ABQ",
            "cover": "https://img.youtube.com/vi/4NRXx6U8ABQ/hqdefault.jpg",
            "platform": "youtube",
        },
        {
            "title": "Treat You Better",
            "artist": "Shawn Mendes",
            "id": "lY2yjEUioBk",
            "cover": "https://img.youtube.com/vi/lY2yjEUioBk/hqdefault.jpg",
            "platform": "youtube",
        },
        {
            "title": "Control",
            "artist": "Armaan Malik",
            "id": "3Xh5V0gP_Yg",
            "cover": "https://img.youtube.com/vi/3Xh5V0gP_Yg/hqdefault.jpg",
            "platform": "youtube",
        },
        {
            "title": "Calm Down",
            "artist": "Selena Gomez, Rema",
            "id": "WcI7uH5kWv8",
            "cover": "https://img.youtube.com/vi/WcI7uH5kWv8/hqdefault.jpg",
            "platform": "youtube",
        },
    ],
    "sad": [
        {
            "title": "Saturn",
            "artist": "SZA",
            "id": "LDZX4ooRsWs",
            "cover": "https://img.youtube.com/vi/LDZX4ooRsWs/hqdefault.jpg",
            "platform": "youtube",
        },
        {
            "title": "Without Me",
            "artist": "Halsey",
            "id": "ZAfAud_M_mg",
            "cover": "https://img.youtube.com/vi/ZAfAud_M_mg/hqdefault.jpg",
            "platform": "youtube",
        },
        {
            "title": "In My Blood",
            "artist": "Shawn Mendes",
            "id": "3KkJxqpmPeU",
            "cover": "https://img.youtube.com/vi/3KkJxqpmPeU/hqdefault.jpg",
            "platform": "youtube",
        },
        {
            "title": "Happier Than Ever",
            "artist": "Billie Eilish",
            "id": "5GJWxDKyk3A",
            "cover": "https://img.youtube.com/vi/5GJWxDKyk3A/hqdefault.jpg",
            "platform": "youtube",
        },
    ],
    "angry": [
        {
            "title": "Closer",
            "artist": "The Chainsmokers, Halsey",
            "id": "PT2_oL4zSKk",
            "cover": "https://img.youtube.com/vi/PT2_oL4zSKk/hqdefault.jpg",
            "platform": "youtube",
        },
        {
            "title": "Bad Guy",
            "artist": "Billie Eilish",
            "id": "DyDfgMOUjCI",
            "cover": "https://img.youtube.com/vi/DyDfgMOUjCI/hqdefault.jpg",
            "platform": "youtube",
        },
    ],
    "tired": [
        {
            "title": "Symphony",
            "artist": "Zara Larsson",
            "id": "aatr_2Mstr4",
            "cover": "https://img.youtube.com/vi/aatr_2Mstr4/hqdefault.jpg",
            "platform": "youtube",
        },
        {
            "title": "Dil Ko Karaar Aaya",
            "artist": "Armaan Malik",
            "id": "2OEL4P1rlo0",
            "cover": "https://img.youtube.com/vi/2OEL4P1rlo0/hqdefault.jpg",
            "platform": "youtube",
        },
    ],
    "fear": [
        {
            "title": "ocean eyes",
            "artist": "Billie Eilish",
            "id": "viimfQi_pWU",
            "cover": "https://img.youtube.com/vi/viimfQi_pWU/hqdefault.jpg",
            "platform": "youtube",
        }
    ],
    "exhausted": [
        {
            "title": "Die For You",
            "artist": "The Weeknd",
            "id": "CD-E-LDc384",
            "cover": "https://img.youtube.com/vi/CD-E-LDc384/hqdefault.jpg",
            "platform": "youtube",
        }
    ],
}


@app.route("/")
def home():
  return render_template("index.html")


@app.route("/dashboard")
def dashboard():
  return render_template("dashboard.html")


@app.route("/about")
def about():
  return render_template("about.html")


@app.route("/contact")
def contact():
  return render_template("contact.html")


@app.route("/recommend", methods=["POST"])
def recommend():
  data = request.get_json() or {}
  mood = data.get("mood", "neutral").lower()
  if mood == "off":
    mood = "neutral"
  platform = data.get("platform", "youtube").lower()

  if platform == "spotify":
    results = SPOTIFY_RECOMMENDATIONS.get(
        mood, SPOTIFY_RECOMMENDATIONS["neutral"]
    )
  else:
    results = ENGLISH_RECOMMENDATIONS.get(
        mood, ENGLISH_RECOMMENDATIONS["neutral"]
    )

  return jsonify({
      "status": "success",
      "mood": mood,
      "platform": platform,
      "recommendations": results,
  })


@app.route("/search", methods=["POST"])
def search_tracks():
  data = request.get_json() or {}
  query = data.get("query", "").strip()
  platform = data.get("platform", "youtube").lower()

  if not query:
    return jsonify({"status": "error", "message": "Empty search query"})

  query_lower = query.lower()

  if platform == "spotify":
    matched = [
        song
        for song in MASTER_SONG_DATABASE
        if query_lower in song["title"].lower()
        or query_lower in song["artist"].lower()
    ]
    if not matched:
      search_query_encoded = urllib.parse.quote(query)
      matched = [{
          "title": query.title(),
          "artist": "Spotify Search Result",
          "id": f"search/{search_query_encoded}",
          "cover": (
              "https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4?w=200"
          ),
          "platform": "spotify",
      }]
    return jsonify({
        "status": "success",
        "query": query,
        "recommendations": matched,
    })

  try:
    query_string = urllib.parse.urlencode({"search_query": query})
    html_content = urllib.request.urlopen(
        "https://www.youtube.com/results?" + query_string
    )
    video_ids = re.findall(
        r"watch\?v=(\S{11})", html_content.read().decode("utf-8", errors="ignore")
    )

    if video_ids:
      unique_ids = list(dict.fromkeys(video_ids))[:5]
      results = [
          {
              "title": query.title(),
              "artist": "YouTube Audio Track",
              "id": vid,
              "cover": f"https://img.youtube.com/vi/{vid}/hqdefault.jpg",
              "platform": "youtube",
          }
          for vid in unique_ids
      ]
      return jsonify({
          "status": "success",
          "query": query,
          "recommendations": results,
      })
  except Exception as e:
    print("Search error:", e)

  return jsonify({
      "status": "success",
      "query": query,
      "recommendations": ENGLISH_RECOMMENDATIONS["neutral"],
  })


if __name__ == "__main__":
  app.run(debug=True, port=5000)