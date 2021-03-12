//-------------------------------
// use numbers for the colors in game to make it easy to increment and randomize
// 0 = blue, 1 = green, 2 = orange, 3 = purple, 4 = red, 5 = yellow
//method 1 - chooses the random numbers and places them in an array.
//method 2 - take user input and compare to method 1 array. return hits and misses ect.
//method main - loop method 2 until lives run out or game is won. this is where visuals should probably go.





//--------------------------------
import java.util.Arrays;
import java.util.Scanner;

public class MasterMind {

    public static void main(String[] args){
        int count = 0;
        int[] MasterArray = Arrays.copyOf(set(), 4);
        for (int x = 0; x < 10; x++) {
            int[] arr = Arrays.copyOf(MasterArray, 4);
            count += 1;
            int count1 = 0;
            int count2 = 0;
            int[] guess = Arrays.copyOf(guess(), 4);
            for (int i = 0; i < 4; i++) {
                if (arr[i] == guess[i]) {
                    count1 += 1;
                }
            }

            for (int j = 0; j < 4; j++) {
                for (int t = 0; t < 4; t++) {
                    if (guess[j] == arr[t]) {
                        arr[t] = t + 100;
                        count2 += 1;
                    }
                }
            }
            if (count1 == 4) {
                System.out.println("you win the game!");
                break;
            }
            int num = 4 - count2;
            System.out.println("correct spot and number : " + count1 + " correct number: " + (count2 - count1) + " incorrect: " + num);

            if (count == 10){
                System.out.println("you lost the game.");
                break;
            }
        }

    }

    public static int[] set(){
         int[] MasterArray = new int[4];
         for (int i = 0; i < 4; i++){
             int Random = (int)(Math.random()*6);
             MasterArray[i] = Random;
         }
         System.out.println(Arrays.toString(MasterArray));
         return MasterArray;
    }

    public static int[] guess(){
        Scanner console = new Scanner(System.in);
        int[] guess = new int[4];
        System.out.print("Type in four numbers between 0 and 5 with spaces to guess: ");
        for (int i = 0; i < 4; i++){
            guess[i] = console.nextInt();

        }
        return guess;
    }


}
