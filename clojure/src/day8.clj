(ns day8
  (:require
   [clojure.string :as str]
   [clojure.test :as t]))

(def example-in (str/split-lines "be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"))

(defn permutations 
  [colls]
  (if (= 1 (count colls))
    (list colls)
    (for [head colls
          tail (permutations (disj (set colls) head))]
      (cons head tail))))

(defn
  split-line
  {:test #(t/is
           (= [[[\a \b \c] [\d \e]] [[\f \g \h] [\i \j]]]
              (split-line "abc de | fgh ij")))}
  [line]
  (->> (str/split line #"\s+")
       (map str/trim)
       (map seq)
       (split-with (partial not= '(\|)))
       ((fn [ln] (list (first ln) (rest (last ln)))))))

(defn get-all-combos
  []
  (->> (permutations (map char (range 97 104)))
       (map #(zipmap [:top :top-left :top-right :middle :bottom-left :bottom-right :bottom] %1))))

(defn correct-combo?
  [m signal-patterns]
  (and
   (= (set (first (filter #(= 2 (count %1)) signal-patterns)))
      (set (vals (select-keys m [:top-right :bottom-right]))))
   (= (set (first (filter #(= 3 (count %1)) signal-patterns)))
      (set (vals (select-keys m [:top-right :bottom-right :top]))))
   (= (set (first (filter #(= 4 (count %1)) signal-patterns)))
      (set (vals (select-keys m [:top-left :top-right :middle :bottom-right]))))
   (every?
    #(or (= (set %1)
            (set (vals (select-keys m [:top :top-right :middle :bottom-left :bottom]))))
         (= (set %1)
            (set (vals (select-keys m [:top :top-right :middle :bottom-right :bottom]))))
         (= (set %1)
            (set (vals (select-keys m [:top :top-left :middle :bottom-right :bottom])))))
    (filter #(= 5 (count %1)) signal-patterns))
   (every?
    #(or (= (set %1)
            (set (vals (select-keys m [:top :top-left :top-right :bottom-left :bottom-right :bottom]))))
         (= (set %1)
            (set (vals (select-keys m [:top :top-left :middle :bottom-left :bottom-right :bottom]))))
         (= (set %1)
            (set (vals (select-keys m [:top :top-left :top-right :middle :bottom-right :bottom])))))
    (filter #(= 6 (count %1)) signal-patterns))
   (= (set (first (filter #(= 7 (count %1)) signal-patterns)))
      (set (vals (select-keys m [:top :top-left :top-right :middle :bottom-left :bottom-right :bottom]))))))

(defn signal-patterns-to-board
  {:test #(t/is (=
                 {:top \d :top-left \e :top-right \a :middle \f :bottom-left \g :bottom-right \b :bottom \c}
                 (signal-patterns-to-board '((\a \c \e \d \g \f \b) (\c \d \f \b \e) (\g \c \d \f \a) (\f \b \c \a \d) (\d \a \b) (\c \e \f \a \b \d) (\c \d \f \g \e \b) (\e \a \f \b) (\c \a \g \e \d \b) (\a \b)))))}
  [signal-patterns]
  (let [foo (filter #(correct-combo? %1 signal-patterns) (get-all-combos))]
    (first foo)))

(defn board-to-map
  {:test #(t/is (= {#{\a \c \e \d \g \f \b} 8
                    #{\c \d \f \b \e} 5
                    #{\g \c \d \f \a} 2
                    #{\f \b \c \a \d} 3
                    #{\d \a \b} 7
                    #{\c \e \f \a \b \d} 9
                    #{\c \d \f \g \e \b} 6
                    #{\e \a \f \b} 4
                    #{\c \a \g \e \d \b} 0
                    #{\a \b} 1}
                   (board-to-map {:top \d :top-left \e :top-right \a :middle \f :bottom-left \g :bottom-right \b :bottom \c})))}
  [board]
  {(set (map board [:top-right :bottom-right])) 1
   (set (map board [:top :top-right :middle :bottom-left :bottom])) 2
   (set (map board [:top :top-right :middle :bottom-right :bottom])) 3
   (set (map board [:top-left :top-right :middle :bottom-right])) 4
   (set (map board [:top :top-left :middle :bottom-right :bottom])) 5
   (set (map board [:top :top-left :middle :bottom-left :bottom-right :bottom])) 6
   (set (map board [:top-right :bottom-right :top])) 7
   (set (map board [:top :top-left :top-right :middle :bottom-left :bottom-right :bottom])) 8
   (set (map board [:top :top-left :top-right :middle :bottom-right :bottom])) 9
   (set (map board [:top :top-left :top-right :bottom-left :bottom-right :bottom])) 0})


(defn get-output-val
  [m o]
  (->> o
       (map set)
       (map m)
       (map str)
       (reduce str)
       (#(Integer/parseInt %1))))

(defn process-line
  [entry]
  (let [[signal-patterns digital-output] entry
        lookup-board (signal-patterns-to-board signal-patterns)
        lookup-map (board-to-map lookup-board)
        line-num (get-output-val lookup-map digital-output)]
    line-num))

(defn solve
  {:test #(t/is (= 61229 (solve example-in)))}
  [lines]
  (->> lines
       (map split-line)
       (map process-line)
       (apply +)))

(t/run-tests)
