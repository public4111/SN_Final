import java.io.*;
import java.util.*;

/**
 * Created by szeyiu on 12/18/14.
 */
public class Graph {
    public double[][] mat;
    public int numOfNodes;
    public int lastNode;
    public int numOfNodesMax;
    public long numOfEdgesW;


    public int INIT_WEIGHT = 100;
    public double DECAY_FACTOR = 1.2;
    public double P = 0.8;
    public int MIN_CONN = 5;


    private void GraphInit(){
        numOfNodesMax = 2000;
        mat = new double[numOfNodesMax][numOfNodesMax];
        for(int i=0; i<numOfNodesMax; ++i){
            for(int j=0; j<numOfNodesMax; ++j)
                mat[i][j] = 0;
        }
        lastNode = -1;
        numOfNodes = 0;
        numOfEdgesW = 0;
    }

    public Graph(){
        GraphInit();
    }

    public boolean[] newVisit(){
        boolean[] bmap = new boolean[lastNode+1];
        for(int i=0; i<bmap.length; ++i){
            bmap[i] = false;
        }
        return bmap;
    }

    public int newNode(){
        lastNode++;
        numOfNodes++;
        return lastNode;
    }

    public boolean newEdge(int src, int dst, double weight){
        if(src>lastNode||dst>lastNode||src<0||dst<0) return false;
        mat[src][dst] = weight;
        mat[dst][src] = weight;
        numOfEdgesW+=weight;
        return true;
    }

    public double w(int src, int dst){
        if(src>lastNode||dst>lastNode||src<0||dst<0) return -1;
        return mat[src][dst];
    }

    public double[] adj(int node){
        if(node>lastNode||node<0) return null;
        double[] result = new double[lastNode+1];
        for(int i=0;i<result.length;++i){
            result[i] = mat[node][i];
        }
        return result;
    }

    public List<Integer> adjList(int node){
        if(node>lastNode||node<0) return null;
        List<Integer> lst = new ArrayList<Integer>();
        for(int i=0;i<=lastNode;++i){
            if(mat[node][i]>0) lst.add(i);
        }
        return lst;
    }

    public int randPickNode() {
        Random random = new Random();
        return random.nextInt(lastNode + 1);
    }

    private void clear(){
        GraphInit();
    }

    public void generate() throws Exception{
        clear();
        int a = newNode();
        int b = newNode();
        newEdge(a,b,INIT_WEIGHT);

        int maxNode = 500;
        int iter = 1;
        while(iter<maxNode) {
            if(iter%50==0){
                printGraph("Graph_"+iter+".txt");
            }
            printInfo();
            newNodeCon();
            iter++;
        }
    }

    public int newNodeCon(){
        int rand = randPickNode();
        int newNode = newNode();
        double weight = avgDegree(rand);
        newEdge(newNode,rand,weight);
        boolean[] visit = newVisit();
        visit[rand] = true;
        bfs(newNode, rand, visit, 1000);
        return newNode;
    }

    private void bfs(int src, int start, boolean[] visit, int maxIter){
        Queue<Integer> q = new LinkedList<Integer>();
        q.offer(-1);
        q.offer(start);
        int layer = -1;
        while(!q.isEmpty()){
            if(layer>maxIter) return;
            int cur = q.poll();
            if(cur==-1){
                layer++;
                if(q.isEmpty()) break;
                q.offer(cur);
                continue;
            }

            List<Integer> adj = adjList(cur);
            List<Integer> toConnect = new ArrayList<Integer>();

            if(adj.size()<=MIN_CONN){
                toConnect.addAll(adj);
            }
            else {
                for (int a : adj) {
                    if (randBoolean(P)) toConnect.add(a);
                }

                for(int i=0; i<adj.size() && toConnect.size()<MIN_CONN;++i){
                    if(!toConnect.contains(adj.get(i))) toConnect.add(adj.get(i));
                }
            }

            for(int a: toConnect){
                if(visit[a]) continue;
                visit[a] = true;
                double w = weakWeight(w(cur, a), layer);
                if(w<1) continue;
                newEdge(src, cur, w);
                q.offer(a);
            }
        }
    }

    private boolean randBoolean(double prob){
        Random random = new Random();
        double r = random.nextDouble();
        return r<prob;
    }

    // this is configurable
    private double weakWeight(double weight, int layer){
        return weight/Math.pow(DECAY_FACTOR,layer);
    }


    private double avgDegree(int node){
        double[] adj = adj(node);
        double result = 0;
        int count = 0;
        for(int i=0; i<adj.length;++i){
            if(adj[i]>0) count++;
            result += adj[i];
        }
        result/=count;
        return result;
    }

    public void printInfo(){
        System.out.println(numOfNodes+" "+numOfEdgesW);
    }

    public void printGraph(String file) throws Exception{
        File f = new File(file);
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(f)));
        for(int i=0; i<=lastNode; ++i){
            for(int j=i+1; j<=lastNode; ++j){
                if(mat[i][j]>0){
                    writer.write(i+" "+j+"\n");
                }
            }
        }
        writer.flush();
        writer.close();
    }

    public void printDegree() throws Exception{
        File f = new File("degree.txt");
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(f)));
        Map<Integer, Integer> dmap = new HashMap<Integer, Integer>();
        for(int i=0; i<=lastNode;++i) {
            int sum = 0;
            for(int j=0; j<=lastNode;++j) {
                sum+=mat[i][j];
            }
            int d = sum;
            if (!dmap.containsKey(d)) {
                dmap.put(d, 0);
            }
            dmap.put(d, dmap.get(d) + 1);
        }
        for(int d: dmap.keySet()){
            writer.write(d+" "+dmap.get(d)+"\n");
        }
        writer.flush();
        writer.close();
    }

    public void printDegreePoints() throws Exception {
        File f = new File("degree_points.txt");
        BufferedWriter writer = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(f)));
        Map<Integer, Integer> dmap = new HashMap<Integer, Integer>();
        for (int i = 0; i <= lastNode; ++i) {
            int sum = 0;
            for (int j = 0; j <= lastNode; ++j) {
                sum += mat[i][j];
            }
            writer.write(sum + "\n");
        }
        writer.flush();
        writer.close();
    }


}
