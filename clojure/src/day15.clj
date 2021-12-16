(ns day15
  (:require
   [clojure.string :as str]
   [clojure.test :as t]))

(def example-in (str/split-lines "1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581"))

(defn smush-lines
  [lines]
  (->> lines
       (map #(str/split %1 #""))
       (mapv (fn [ln] (mapv #(Integer/parseInt %1) ln)))))

(defn inc-item
  [item i]
  (let [n (+ item i)] (if (> n 9) (inc (mod (dec n) 9)) n)))

(defn grow-row
  [row-idx row]
  (into [] (map-indexed
   (fn [col-idx item] (inc-item item (+ row-idx (quot col-idx (count row)))))
   (take (* 5 (count row)) (cycle row)))))

;; 0 1 2 3 4
;; 1 2 3 4 5
;; 2 3 4 0 1
;; 3 4 0 1 2
;; 4 0 1 2 3
(defn grow-grid
  {:test #(t/is
          (= [[8 9 1 2 3]
               [9 1 2 3 4]
               [1 2 3 4 5]
               [2 3 4 5 6]
               [3 4 5 6 7]]
             (grow-grid [[8]])))}
  [grid]
  (into [] (map-indexed
   (fn [idx itm] (grow-row (quot idx (count grid)) itm))
   (take (* 5 (count grid)) (cycle grid)))))

(defn get-coord
  {:test #(t/is (= 3 (get-coord '((2 1 9) (3 9 8)) {:x 0 :y 1})))}
  [grid c]
  (let [{x :x y :y} c]
    (nth (nth grid y nil) x nil)))

(defn points-around
  [{x :x y :y}]
  [{:x x :y (inc y)}
   {:x (inc x) :y y}
   {:x (dec x) :y y}
   {:x x :y (dec y)}])

(defn get-neighbours
  [g p]
  (->> (points-around p)
       (map #(assoc %1 :cost (get-coord g %1)))
       (filter #(some? (:cost %1)))))

(defn nodes
  [n]
  (set (mapcat (fn [r] (map (fn [c] (hash-map :x c :y r)) (range n))) (range n))))

(defn next-to-visit
  [unvisited dists]
  (if (empty? unvisited)
    #{}
    (apply min-key #(dists %1) unvisited)))

(defn dijkstra
  [nodes start n-fn]
  (loop [dists (assoc (zipmap nodes (repeat Integer/MAX_VALUE)) start 0)
         unvisited nodes
         curr start]
    (println (count unvisited) "left to visit")
    (if (empty? unvisited)
      dists
      (let [neighbours (n-fn curr)
            new-neighbours (map
                            (fn
                              [neighbour]
                              (update neighbour :cost #(min (+ %1 (dists curr)) (dists (select-keys neighbour [:x :y])))))
                            neighbours)
            new-dst (reduce (fn [acc curr] (assoc acc (select-keys curr [:x :y]) (curr :cost))) dists new-neighbours)
            new-unvisited (disj unvisited curr)]
        (recur new-dst new-unvisited (next-to-visit new-unvisited new-dst))))))

(defn solve
  {:test #(t/is (= 315 (solve example-in)))}
  [lines]
  (let [grid (grow-grid (smush-lines lines)) n (dec (count grid))]
    ((dijkstra (nodes (count grid)) {:x 0 :y 0} (partial get-neighbours grid)) {:x n :y n})))

(t/run-tests)

(defn solve-real
  []
  (solve (str/split-lines (slurp "res/day15"))))
