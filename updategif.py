def updategif(gif_url):
    db.execute("UPDATE Accounts SET profilegif = :profilegif WHERE id = :id", profilegif = gif_url, id = session["user_id"])

    return redirect(url_for("profielpagina"))