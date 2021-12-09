(ns day9
  (:require
   [clojure.test :as t]
   [clojure.string :as str]))

(def example-in (str/split-lines "2199943210
3987894921
9856789892
8767896789
9899965678"))

(defn smush-lines
  [lines]
  (->> lines
       (map #(str/split %1 #""))
       (map (fn [ln] (map #(Integer/parseInt %1) ln)))))

(defn get-coord
  {:test #(t/is (= 3 (get-coord {:x 0 :y 1} '((2 1 9) (3 9 8)))))}
  [c grid]
  (let [{x :x y :y} c] (nth (nth grid y nil) x nil)))

(defn get-adjacents
  {:test #(t/is (= '(3 1 9) (get-adjacents {:x 0 :y 0} '((2 1 9 9) (3 9 8 7)))))}
  [c grid]
  (let [{x :x y :y} c]
    (filter identity [(get-coord {:x (dec x) :y (dec y)} grid)
                      (get-coord {:x (dec x) :y y} grid)
                      (get-coord {:x (dec x) :y (inc y)} grid)
                      (get-coord {:x x :y (dec y)} grid)
                      (get-coord {:x x :y (inc y)} grid)
                      (get-coord {:x (inc x) :y (dec y)} grid)
                      (get-coord {:x (inc x) :y y} grid)
                      (get-coord {:x (inc x) :y (inc y)} grid)])))

(defn low-point?
  [point adjacents]
  (< point (reduce min adjacents)))

(defn ranges
  [x y]
  (mapcat (fn [row] (map (fn [col] {:x col :y row}) (range x))) (range y)))

(defn find-low-points
  [grid]
  (let [xmax (count (first grid)) ymax (count grid)]
    (filter
     #(low-point? (get-coord %1 grid) (get-adjacents %1 grid))
     (ranges xmax ymax))))

(defn mark
  {:test #(t/is (= '(({:v 1 :marked? true})) (mark {:x 0 :y 0} '(({:v 1 :marked? false})))))}
  [point grid]
  (map-indexed
   (fn [row-idx row] (map-indexed (fn [col-idx item]
                                    (if (and (= (point :x) col-idx)
                                             (= (point :y) row-idx))
                                      (assoc item :marked? true)
                                      item)) row))
   grid))

(defn points-around
  [p]
  (let [{x :x y :y} p]
    [{:x (dec x) :y y}
     {:x x :y (dec y)}
     {:x x :y (inc y)}
     {:x (inc x) :y y}]))

(defn mark-recurse
  {:test #(t/is
           (=
            '(({:v 2 :marked? true} {:v 1 :marked? true}) ({:v 3 :marked? true} {:v 9 :marked? false}))
            (mark-recurse {:x 1 :y 0} '(({:v 2 :marked? false} {:v 1 :marked? false}) ({:v 3 :marked? false} {:v 9 :marked? false})))))}
  [point grid]
  (let [marked (mark point grid)
        to-mark (->> (points-around point) 
                     (filter #(some? (get-coord %1 grid)))
                     (filter #((complement :marked?) (get-coord %1 grid)))
                     (filter #(< (:v (get-coord %1 grid)) 9)))]
    (if (empty? to-mark)
      marked
      (reduce (fn [acc curr] (mark-recurse curr acc)) marked to-mark))))

(defn basin-size
  [grid]
  (count (filter :marked? (flatten grid))))

(defn solve
  {:test #(t/is (= 1134 (solve example-in)))}
  [lines]
  (let [grid (smush-lines lines)
        basin-board (map (fn [row] (map (fn [item] {:v item :marked? false}) row)) grid)]
    (->> (find-low-points grid)
         (map #(mark-recurse %1 basin-board))
         (map basin-size)
         (sort)
         (reverse)
         (take 3)
         (apply *))))

(t/run-tests)
