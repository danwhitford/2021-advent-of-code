(ns day4
  (:require
   [clojure.string :as str]
   [clojure.test :as t]))

(def example-in (str/split-lines "7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"))

(defn get-moves
  [line]
  (map #(Integer/parseInt %1) (str/split line #",")))

(defn line-to-ints
  [line]
  (->>
   (map #(Integer/parseInt %1) (str/split (str/trim line) #"\s+"))
   (map #(hash-map :v %1 :marked? false))))

(defn get-boards
  [lines]
  (loop [lines lines board [] boards []]
    (let [line (first lines)]
      (cond
        (nil? line) (conj boards board)
        (and (= "" line) (empty? board)) (recur (rest lines) board boards)
        (= "" line) (recur (rest lines) [] (conj boards board))
        :else (recur (rest lines) (conj board (line-to-ints line)) boards)))))

(defn winning-board?
  [board]
  (or
   (some (fn [row] (every? #(= (:marked? %1) true) row)) board)
   (some (fn [row] (every? #(= (:marked? %1) true) row)) (apply map vector board))
   false))

(defn do-move
  [boards move]
  (map (fn [board]
         (map (fn [row]
                (map (fn [el]
                       (if (= (:v el) move)
                         (merge el {:marked? true}) el))
                     row)) board)) boards))

(defn calculate-winning-score
  [board move]
  (->> board
       (flatten)
       (filter #(not (:marked? %)))
       (map :v)
       (apply +)
       (* move)))

(defn split-by
  [pred coll]
  (let [{true-list true false-list false} (group-by pred coll)]
    (list true-list false-list)))

(defn get-last-win
  [lines]
  (let
   [moves (get-moves (first lines))
    boards (get-boards (rest lines))]
    (loop [active-boards boards moves moves last-win nil]
      (let
       [move (first moves)
        new-boards (do-move active-boards move)
        [winning-boards remaining-boards] (split-by winning-board? new-boards)
        last-win (if (empty? winning-boards) last-win {:move move :board (last winning-boards)})]
        (if (nil? move)
          last-win
          (recur remaining-boards
                 (rest moves)
                 last-win))))))

(defn solve
  {:test #(t/is (= 1924 (solve example-in)))}
  [lines]
  (let [lst (get-last-win lines)]
    (calculate-winning-score (:board lst) (:move lst))))

(t/run-tests)
