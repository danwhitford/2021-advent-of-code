(ns day5
  (:require
   [clojure.string :as str]
   [clojure.test :as t]
   [clojure.set :as st]))

(def example-in (str/split-lines "0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"))

(defn get-from-to
  [line]
  (as-> line $$
    (str/split $$ #" -> |,")
    (map #(Integer/parseInt %1) $$)
    (zipmap [:x1 :y1 :x2 :y2] $$)))

(defn range-2-way
  {:test
   #(t/testing (t/is (= '(2 3 4 5) (range-2-way 2 5)))
     (t/is (= '(10 9 8 7 6 5) (range-2-way 10 5))))}
  [start stop]
  (if (> stop start)
    (range start (inc stop))
    (range start (dec stop) -1)))

(defn expand-line-segment
  {:test #(t/is (= (list {:x 1 :y 5} {:x 2 :y 5} {:x 3 :y 5}) (expand-line-segment {:x1 1 :y1 5 :x2 3 :y2 5})))}
  [seg]
  (let [{x1 :x1 x2 :x2 y1 :y1 y2 :y2} seg]
    (cond
      (= x1 x2) (map #(hash-map :x x1 :y %1) (range-2-way y1 y2))
      (= y1 y2) (map #(hash-map :x %1 :y y1) (range-2-way x1 x2))
      :else (map #(hash-map :x %1 :y %2) (range-2-way x1 x2) (range-2-way y1 y2)))))

(defn straight-line?
  {:test #(t/testing (t/is (straight-line? {:x1 0 :y1 9 :x2 5 :y2 9}))
            (t/is (straight-line? {:x1 0 :y1 9 :x2 0 :y2 5}))
            (t/is (not (straight-line? {:x1 1 :y1 2 :x2 3 :y2 4}))))}
  [seg]
  (let [{x1 :x1 x2 :x2 y1 :y1 y2 :y2} seg]
    (or (= x1 x2) (= y1 y2) false)))

(defn solve
  {:test #(t/is (= 12 (solve example-in)))}
  [lines]
  (let [line-segments (map get-from-to lines)
        points (map expand-line-segment line-segments)]
    (loop [points points covered #{} intersections #{}]
      (let [hd (first points)]
        (if (nil? hd)
          (count intersections)
          (recur
           (rest points)
           (reduce conj covered hd)
           (st/union intersections (st/intersection covered (reduce conj #{} hd)))))))))

(t/run-tests)
