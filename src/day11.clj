(ns day11
  (:require
   [clojure.string :as str]
   [clojure.test :as t]))

(def example-in (str/split-lines "5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526"))
(def all-points (mapcat (fn [row-idx] (map (fn [col-idx] {:x col-idx :y row-idx}) (range 10))) (range 10)))

(defn smush-lines
  [lines]
  (->> lines
       (map #(str/split %1 #""))
       (mapv (fn [ln] (mapv #(Integer/parseInt %1) ln)))))

(defn get-coord
  {:test #(t/is (= 3 (get-coord '((2 1 9) (3 9 8)) {:x 0 :y 1})))}
  [grid c]
  (let [{x :x y :y} c]
    (nth (nth grid y nil) x nil)))

(defn points-around
  [p]
  (let [{x :x y :y} p]
    [{:x x :y (dec y)}
     {:x x :y (inc y)}
     {:x (dec x) :y y}
     {:x (inc x) :y y}
     {:x (dec x) :y (dec y)}
     {:x (dec x) :y (inc y)}
     {:x (inc x) :y (inc y)}
     {:x (inc x) :y (dec y)}]))

(defn mark-point
  [grid point v]
  (let [{x :x y :y} point]
    (update grid y
            (fn [row] (assoc row x v)))))

(defn mark
  {:test #(t/is (=
                 [[:f 2] [2 2]]
                 (mark [[9 1] [1 1]] {:x 0 :y 0})))}
  [grid point]
  (let [v (get-coord grid point)]
    (cond
      (nil? v) grid
      (= v :f) grid
      (= v 9) (reduce mark (mark-point grid point :f) (filter #(some? (get-coord grid %1)) (points-around point)))
      :else (mark-point grid point (inc v)))))

(defn next-gen
  {:test #(t/is
           (= [[3 4 5 4 3] [4 :f :f :f 4] [5 :f :f :f 5] [4 :f :f :f 4] [3 4 5 4 3]]
              (next-gen [[1 1 1 1 1] [1 9 9 9 1] [1 9 1 9 1] [1 9 9 9 1] [1 1 1 1 1]])))}
  [grid]
  (reduce mark grid all-points))

(defn reset-grid
  [grid]
  (mapv (fn [row] (mapv #(if (= % :f) 0 %1) row)) grid))

(defn solve
  {:test #(t/is (= 195 (solve example-in)))}
  [lines]
  (let [grid (smush-lines lines)]
    (loop [grid grid gen 1]
      (when (> gen 1000) (assert false))
      (prn "Gen:" gen)
      (let [
            stepped (next-gen grid)
            total-flashes (count (filter #(= %1 :f) (flatten stepped)))]
        (prn "Flashes:" total-flashes)
        (if (= total-flashes 100)
          gen
          (recur (reset-grid stepped) (inc gen)))))))

(t/run-tests)