// Command validate checks index.json and every design with the same parser the
// CaseHUD app uses. It must live inside a CaseHUD checkout (internal packages),
// see .github/workflows/validate.yml. Usage: validate <repo-dir>
package main

import (
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"regexp"
	"strings"

	"github.com/kewe87/casehud/internal/community"
)

var idRe = regexp.MustCompile(`^[a-z0-9][a-z0-9-]{0,47}$`)

func main() {
	if len(os.Args) != 2 {
		fmt.Fprintln(os.Stderr, "usage: validate <repo-dir>")
		os.Exit(2)
	}
	root := os.Args[1]
	bad := 0
	fail := func(f string, a ...any) { bad++; fmt.Printf("FAIL: "+f+"\n", a...) }

	b, err := os.ReadFile(filepath.Join(root, "index.json"))
	if err != nil {
		fmt.Println(err)
		os.Exit(1)
	}
	if len(b) > 1<<20 {
		fail("index.json larger than 1 MiB")
	}
	var idx struct {
		Version int                `json:"version"`
		Designs []community.Entry `json:"designs"`
	}
	if err := json.Unmarshal(b, &idx); err != nil {
		fmt.Println("index.json:", err)
		os.Exit(1)
	}
	if idx.Version != 1 {
		fail("index.json: version must be 1")
	}
	seen, files := map[string]bool{}, map[string]bool{}
	for _, e := range idx.Designs {
		if !idRe.MatchString(e.ID) {
			fail("%q: invalid id (a-z, 0-9, -; max 48 chars)", e.ID)
		}
		if seen[e.ID] {
			fail("%s: duplicate id", e.ID)
		}
		seen[e.ID] = true
		if e.Name == "" || e.Author == "" {
			fail("%s: name and author are required", e.ID)
		}
		clean := filepath.ToSlash(filepath.Clean(e.File))
		if !strings.HasPrefix(clean, "designs/") || !strings.HasSuffix(clean, ".json") || strings.Contains(e.File, "..") || strings.Contains(e.File, "://") {
			fail("%s: file must be designs/<name>.json, got %q", e.ID, e.File)
			continue
		}
		files[clean] = true
		d, err := os.ReadFile(filepath.Join(root, filepath.FromSlash(clean)))
		if err != nil {
			fail("%s: %v", e.ID, err)
			continue
		}
		if len(d) > 256<<10 {
			fail("%s: design larger than 256 KiB", e.ID)
			continue
		}
		l, err := community.Parse(d)
		if err != nil {
			fail("%s: %v", e.ID, err)
			continue
		}
		if l.Round != e.Round {
			fail("%s: index round=%v but design round=%v", e.ID, e.Round, l.Round)
		}
		fmt.Printf("ok   %-22s %dx%d, %d widgets\n", e.ID, l.Width, l.Height, len(l.Widgets))
	}
	all, _ := filepath.Glob(filepath.Join(root, "designs", "*.json"))
	for _, f := range all {
		if rel := "designs/" + filepath.Base(f); !files[rel] {
			fail("%s is not listed in index.json", rel)
		}
	}
	if bad > 0 {
		fmt.Printf("%d problem(s)\n", bad)
		os.Exit(1)
	}
}
