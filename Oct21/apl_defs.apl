⍝ Full October 2021 JS solution in APL.
⍝ This works by creating n array from 0 to n that will calculate the odds of n races being picked in 3*n - 1 choices.
⍝ If less than n races are chosen in 3n-1 picks, we win


⍝ Creates initial probability array after first bot picks race
f ← 1=⍳

⍝ Probability array after next bots pick race
pickRace ← (⊣×((⍳≢)÷≢))+(¯1⌽(⊣×(1-((⍳≢)÷≢))))

⍝ Repeats pickRace for every bot except us
probs ← {pickRace⍣((3×⍵)-2)f ⍵}

⍝ Gets the odds of at least one race being empty
winrate ← ¯1↑(1-probs)

⍝ Given a winrate, calculates minimum n that gives you a winrate greater than it
solution ← {                            
     ⍺←2                     
     ⍵≥1:'Infeasible' ⋄      
     (winrate ⍺)<⍵:(⍺+1)∇ ⍵ ⋄
     ⍺,winrate(⍺)            
 }   
 
⍝ Gross way to visualise the "probability cascade", i.e the repeated iterations of pickrace from the initial 1 0 ... 0 vector.
 createTable ← {↑⍵{pickRace⍣⍵ f ⍺}¨(⍳(3×⍵)-1)-1}
 
⍝ This pops out the solution 
solution ÷3
