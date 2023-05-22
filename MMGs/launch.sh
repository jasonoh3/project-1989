#chmod +x launch.sh

session="launch"
main() {
    tmux new -A -d -s $session
    
    tmux neww -dn cat
    tmux neww -dn dog
    tmux neww -dn uiuc
    tmux neww -dn korea
    tmux neww -dn memes
    tmux neww -dn burger
    tmux neww -dn movies
    tmux neww -dn nature
    tmux neww -dn amongus
    tmux neww -dn pokemon
    tmux neww -dn reducer
    tmux neww -dn nintendo
    tmux neww -dn painting
    tmux neww -dn vegetable

    tmux send -t "cat" "python3 cat.py" C-m
    tmux send -t "dog" "python3 dog.py" C-m
    tmux send -t "uiuc" "python3 uiuc.py" C-m
    tmux send -t "korea" "python3 korea.py" C-m
    tmux send -t "memes" "python3 memes.py" C-m
    tmux send -t "burger" "python3 burger.py" C-m
    tmux send -t "movies" "python3 movies.py" C-m
    tmux send -t "nature" "python3 nature.py" C-m
    tmux send -t "amongus" "python3 amongus.py" C-m
    tmux send -t "pokemon" "python3 pokemon.py" C-m
    tmux send -t "reducer" "python3 reducer.py" C-m
    tmux send -t "nintendo" "python3 nintendo.py" C-m
    tmux send -t "painting" "python3 painting.py" C-m
    tmux send -t "vegetable" "python3 vegetable.py" C-m

    tmux a -t $session
}

main