package handler

import (
	"net/http"

	"github.com/goth-ecosystem/goth/gothic"
	"github.com/markbates/goth"
	"github.com/markbates/goth/providers/github"
	"os"
)

func init() {
	goth.UseProviders(
		github.New(os.Getenv("GITHUB_CLIENT_ID"), os.Getenv("GITHUB_CLIENT_SECRET"), os.Getenv("CALLBACK_URL")),
	)
}

func Handler(w http.ResponseWriter, r *http.Request) {
	// try to get the user without re-authenticating
	if gothUser, err := gothic.CompleteUserAuth(w, r); err == nil {
		// TODO: send token to client
		_ = gothUser
	} else {
		gothic.BeginAuthHandler(w, r)
	}
}