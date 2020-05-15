import java.io.IOException;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.io.FloatWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;
import org.apache.hadoop.mapreduce.Mapper;
import org.apache.hadoop.mapreduce.Reducer;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.util.GenericOptionsParser;
import java.util.Map;
import java.io.IOException;

public class AvgExp {
	public static class Map extends Mapper<Object, Text, Text, FloatWritable> {
        protected void map(Object offset, Text rows, Context context) throws IOException, InterruptedException {
        	String[] cols = rows.toString().split(",");
        	if (Float.parseFloat(cols[8].replace("'",""))>10000.00) {
        		context.write(new Text(cols[2]), new FloatWritable(Float.parseFloat(cols[7].replace("'",""))));
        	}      
        }
    }

	public static class Reduce extends Reducer<Text, FloatWritable, Text, FloatWritable> {
	    protected void reduce(Text key, Iterable<FloatWritable> values, Context context) throws IOException, InterruptedException {
	        float sum = 0;
	        int count = 0;
	        for (FloatWritable value : values){
                sum += value.get();
	        	count++;
            }
	            
	        float avg = sum/count;
	        if (count>=5) {
	        	context.write(key, new FloatWritable(avg));
	        }
	        
	    }
	}

	public static void main(String[] args) throws Exception {
	    Configuration conf = new Configuration();
		Job job = Job.getInstance(conf, "AvgExp");
	    job.setJarByClass(AvgExp.class);
	    job.setOutputKeyClass(Text.class);
	    job.setOutputValueClass(FloatWritable.class);
	    job.setMapperClass(Map.class);
	    job.setReducerClass(Reduce.class);
	    job.setInputFormatClass(TextInputFormat.class);
	    job.setOutputFormatClass(TextOutputFormat.class);
	    job.setNumReduceTasks(1);
	
	    FileInputFormat .setInputPaths(job, new Path(args[0]));
	    FileOutputFormat.setOutputPath(job, new Path(args[1]));
	
	    boolean success = job.waitForCompletion(true);
	    System.out.println(success);
	}
	
}
	
