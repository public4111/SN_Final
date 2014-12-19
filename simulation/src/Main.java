public class Main {

    public static void main(String[] args) throws Exception {
        Graph G = new Graph();
        G.generate();
        G.printDegree();
        G.printDegreePoints();
    }
}
