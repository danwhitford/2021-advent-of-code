(ns day7
  (:require
   [clojure.string :as str]
   [clojure.test :as t]))

(def example-in (str/split-lines "16,1,2,0,4,2,7,1,2,14"))

(defn abs [x]
  (if (< x 0) (- x) x))

(defn difference
  [a b]
  (abs (- a b)))

(defn cost
  [a b]
  (let [n (difference a b)]
    (/ (* n (inc n)) 2)))

(defn get-cost-to-move
  {:test #(t/is (= 206 (get-cost-to-move 2 '(16 1 2 0 4 2 7 1 2 14))))}
  [pos-to-align line]
  (apply + (map (partial cost pos-to-align) line)))

(defn solve
  {:test #(t/is (= 168 (solve example-in)))}
  [lines]
  (let
   [line (map #(Integer/parseInt %) (str/split (first lines) #","))
    smallest (reduce min line)
    biggest (reduce max line)]
    (->> (map #(get-cost-to-move %1 line) (range smallest (inc biggest)))
         (reduce min))))

(t/run-tests)
