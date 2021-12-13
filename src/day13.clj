(ns day13
  (:require
   [clojure.string :as str]
   [clojure.test :as t]))

(def example-in (str/split-lines "6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5"))

(defn get-dots
  [lines]
  (->> lines
       (take-while #(> (count %1) 0))
       (map #(str/split %1 #","))
       (map (fn [ln] (map (fn [n] (Integer/parseInt n)) ln)))
       (map #(hash-map :x (first %1) :y (second %1)))
       (set)))

(defn get-grid
  [lines]
  (let [dots (get-dots lines)
        xmax (reduce max (map :x dots))
        ymax (reduce max (map :y dots))]
    (mapv (fn [y-idx] (mapv
                       (fn [x-idx] (contains? dots {:x x-idx :y y-idx}))
                       (range (inc xmax))))
          (range (inc ymax)))))

(defn get-folds
  [lines]
  (->> lines
       (drop-while #(not (str/starts-with? %1 "fold along")))
       (map #(str/split %1 #"fold along "))
       (map last)
       (map #(str/split %1 #"="))
       (map #(hash-map :axis (first %1) :at (Integer/parseInt (second %1))))))

(defn merge-row
  {:test #(t/is (= [true false true false true true false]
                   (merge-row '(true false true false false) '(false false true false true true false))))}
  [a b]
  (loop [[ahd & arst] a [bhd & brst] b ret []]
    (if (and (nil? ahd) (nil? bhd))
      ret
      (recur arst brst (conj ret (or ahd bhd))))))

(defn merge-rows
    {:test #(t/is (= [[true false true]]
                   (merge-rows [[false false false]] [[true false true]])))}
  [a b]
  (loop [[ahd & arst] a [bhd & brst] b ret []]
    (if (and (nil? ahd) (nil? bhd))
      ret
      (recur arst brst (conj ret (merge-row ahd bhd))))))

(defn tear-at
  {:test #(t/is (= [[1 2 3] [5 6 7]] (tear-at 3 [1 2 3 4 5 6 7])))}
  [n col]
  [(take n col) (drop (inc n) col)])

(defn fold-left
  {:test #(t/is (=
                 [[true][false][true]]
                 (fold-left [[true false true] [false false false] [false false true]] 1)))}
  [g at]
  (mapv 
   (fn [row] (let [[l r] (tear-at at row)] (merge-row (reverse l) r))) 
   g))

(defn fold-up
  {:test #(t/is (=
                 [[true false true]]
                 (fold-up [[true false true] [false false false] [false false true]] 1)))}
  [g at]
  (let [[t b] (tear-at at g)]
    (merge-rows (reverse t) b)))

(defn pprint-grid
  [grid]
  (doseq [ln (reverse grid)]
    (prn (str/join " " (map #(if %1 "#" ".") (reverse ln))))))

(defn fold
  [g fold]
  (if (= "x" (fold :axis))
    (fold-left g (fold :at))
    (fold-up g (fold :at))))

(defn solve
  {:test #(t/is (= nil (solve example-in)))}
  [lines]
  (let [grid (get-grid lines)
        folds (get-folds lines)]
    (pprint-grid (reduce fold grid folds))))

(solve example-in)
(t/run-tests)
